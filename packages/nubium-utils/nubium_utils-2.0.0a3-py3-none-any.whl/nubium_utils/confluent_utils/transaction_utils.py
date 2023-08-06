from .consumer_utils import get_transactional_consumer, consume_message, get_consumer
from .message_utils import shutdown_cleanup
from .producer_utils import get_transactional_producer, produce_message
from nubium_utils.general_utils import parse_headers
from confluent_kafka import TopicPartition
from nubium_utils.confluent_utils.confluent_configs import init_schema_registry_configs
from nubium_utils.custom_exceptions import NoMessageError
import logging
import sys
# from orjson import dumps, loads
# changelog_schema = {"type": "bytes"}
from json import dumps, loads
changelog_schema = {"type": "string"}
from random import random

from copy import deepcopy
from nubium_utils.confluent_utils.rocksb_utils import RDB
from os import environ
from time import sleep

LOGGER = logging.getLogger(__name__)

class RunTableRecovery(Exception):
    def __init__(self):
        pass

class Transaction:
    def __init__(self, message, producer, consumer, metrics_manager):
        self.producer = producer
        self.consumer = consumer
        self.metrics_manager = metrics_manager
        self.message = message
        
        self._committed = False
        self._active_transaction = False

    def key(self):
        return self.message.key()

    def value(self):
        return self.message.value()

    def headers(self):
        return parse_headers(self.message.headers())

    def topic(self):
        return self.message.topic()

    def partition(self):
        return self.message.partition()

    def offset(self):
        return self.message.offset()

    def produce(self, producer_kwargs):
        self.producer.poll(0)
        if not self._active_transaction:
            self.producer.begin_transaction()
            self._active_transaction = True
        produce_message(self.producer, producer_kwargs, self.metrics_manager, self.headers())
        self.producer.poll(0)

    def commit(self, mark_committed=True):
        if self._active_transaction:
            self.producer.send_offsets_to_transaction(
                [TopicPartition(self.topic(), self.partition(), self.offset() + 1)], self.consumer.consumer_group_metadata())
            self.producer.commit_transaction()
            self.producer.poll(0)
            self._committed = mark_committed


class TableTransaction(Transaction):
    def __init__(self, message, producer, consumer, metrics_manager, changelog_topic):
        self.message = message
        self.changelog_topic = changelog_topic

        self._changelog_updated = False
        self._pending_table_write = None

        super().__init__(self.message, producer, consumer, metrics_manager)

    def read_table_entry(self):
        return self._rdb_read()
        
    def update_table_entry(self, value):
        self._pending_table_write = deepcopy(value)
        if isinstance(self._pending_table_write, (list, dict)):
            # LOGGER.debug(f'attempting json dumps of {self._pending_table_write}')
            self._pending_table_write = dumps(self._pending_table_write)

    def delete_table_entry(self):
        self._pending_table_write = '-DELETED-'
        
    def _update_changelog(self):
        self.produce(dict(
            topic=self.changelog_topic,
            key=self.key(),
            value=self._pending_table_write
        ))
        self._changelog_updated = True
        self.producer.poll(0)

    def _recover_table_via_changelog(self):
        value = self.value()
        try:
            value = loads(value)
        except:
            pass
        if value == '-DELETED-':
            self.delete_table_entry()
        else:
            self.update_table_entry(value)
        super().commit()
        self._rdb_write(self._pending_table_write)

    def _rdb_write(self, value):
        if self._pending_table_write == '-DELETED-':
            LOGGER.debug('Finalizing table entry delete...')
            rdb_tables[self.partition()].delete(self.key())
            rdb_tables[self.partition()].write('offset', str(self._rdb_offset() + 2))
        else:
            # LOGGER.debug(f'Finalizing table entry write:\npartition{self.partition()},\nkey:{self.key()},\nvalue:{self._pending_table_write}...')
            LOGGER.debug(f'Finalizing table entry write:\npartition{self.partition()},\nkey:{self.key()}')
            rdb_tables[self.partition()].write_batch(
                {self.key(): self._pending_table_write,
                 'offset': str(self._rdb_offset() + 2)})
        self._pending_table_write = None

    def _rdb_read(self):
        value = rdb_tables[self.partition()].read(self.key())
        try:
            value = loads(value)
        except:
            pass
        LOGGER.debug(f'Read table value: {value}')
        return value

    def _rdb_offset(self):
        value = rdb_tables[self.partition()].read('offset')
        if not value:
            value = self.offset() if self.offset() else 0
        return int(value)
    
    def commit(self):
        if not self._changelog_updated and self._pending_table_write:
            self._update_changelog()
        super().commit(mark_committed=False)
        if self._pending_table_write:
            self._rdb_write(self._pending_table_write)


class TransactionApp:
    def __init__(self, app_function, consume_topics_list, produce_topic_schema_dict, 
                 metrics_manager=None, schema_registry=None, cluster=None, consumer=None, producer=None):
        self.app_function = app_function
        self.metrics_manager = metrics_manager
        if not schema_registry:
            self.schema_registry = init_schema_registry_configs(as_registry_object=True)
        if not consumer:
            self.consumer = get_transactional_consumer(consume_topics_list, self.schema_registry, cluster=cluster)
        if not producer:
            self.producer = get_transactional_producer(produce_topic_schema_dict, self.schema_registry, cluster=cluster)

    def consume(self, timeout=None):
        return consume_message(self.consumer, self.metrics_manager, timeout)

    def run(self, *args, **kwargs):
        try:
            while True:
                transaction = None
                try:
                    transaction = Transaction(self.consume(), self.producer, self.consumer, self.metrics_manager)
                    self.app_function(transaction, *args, **kwargs)
                    if not transaction._committed:
                        transaction.commit()
                except NoMessageError:
                    self.producer.poll(0)
                except Exception as e:
                    raise
        finally:
            # TODO: might need to move the transaction abort within the while loop. 
            if transaction:
                if transaction._active_transaction:
                    self.producer.abort_transaction(10)
            shutdown_cleanup(consumer=self.consumer)


class TableApp(TransactionApp):
    def __init__(self, app_function, consume_topics_list, produce_topic_schema_dict, 
                 metrics_manager=None, schema_registry=None, cluster=None, consumer=None, producer=None):
        self.changelog_topic = f"{environ['APP_NAME']}__changelog"
        if self.changelog_topic not in produce_topic_schema_dict:
            produce_topic_schema_dict.update({self.changelog_topic: changelog_schema})
        global rdb_tables
        rdb_tables = {}
        if not schema_registry:
            self.schema_registry = init_schema_registry_configs(as_registry_object=True)
        if not consumer:
            self.consumer = self._set_table_consumer(consume_topics_list, self.schema_registry, cluster=cluster)
        super().__init__(
            app_function, consume_topics_list, produce_topic_schema_dict,
            metrics_manager=metrics_manager, schema_registry=schema_registry, cluster=cluster, consumer=self.consumer, producer=producer)

    def _set_table_consumer(self, topic, schema_registry, default_schema=None, cluster=None):
        consumer = get_transactional_consumer(topic, schema_registry, default_schema, False, cluster)
        setattr(consumer, 'topic', topic)
        setattr(consumer, 'changelog_topic', self.changelog_topic)
        setattr(consumer, 'table_recovery_status', {})
        setattr(consumer, 'pending_primary_partitions', [])
        setattr(consumer, 'pending_recovery_partitions', {})
        consumer.subscribe([topic], on_assign=_rocksdb_assign, on_revoke=_rocksdb_unassign, on_lost=_rocksdb_unassign)
        LOGGER.debug('Table consumer initialized')
        return consumer
    
    def _check_changelog_offset(self):
        self.consumer.position()
    
    # def _table_recovery(self):
    #     checks_left = 2
    #     # TODO: This while loop may not be necc anymore since I'm doing the exception approach now
    #     while not self.consumer.table_recovery_status or checks_left:
    #         try:
    #             # Must poll with consumer to ensure all data on the consumer object is properly populated
    #             transaction = TableTransaction(self.consume(timeout=2), self.producer, self.consumer,
    #                                            self.metrics_manager, self.changelog_topic)
    #             # Once the consumer is appropriately populated...
    #             checks_left = 0
    #         except NoMessageError:
    #             LOGGER.debug('Still waiting for table transaction status...')
    #             checks_left -= 1
    #     LOGGER.debug(f'table_recovery_status before recovery attempt: {self.consumer.table_recovery_status}')
    #     LOGGER.debug(f'pending_recovery_partitions before recovery attempt: {self.consumer.pending_recovery_partitions}')
    #     seek_list = [p_obj for p, p_obj in self.consumer.pending_recovery_partitions.items() if p in self.consumer.table_recovery_status]
    #     for p_obj in seek_list:
    #         self.consumer.seek(p_obj)
    #     if self.consumer.table_recovery_status:
    #         LOGGER.info('BEGINNING TABLE RECOVERY PROCEDURE')
    #         checks_left = 2
    #         while (checks_left and self.consumer.table_recovery_status):
    #             try:
    #                 transaction = TableTransaction(self.consume(timeout=3), self.producer, self.consumer, self.metrics_manager,
    #                                                self.changelog_topic)
    #                 LOGGER.debug(f'Recovery write is {transaction.value()}')
    #                 transaction._recover_table_via_changelog()
    #                 p = transaction.partition()
    #                 LOGGER.debug(f"transaction_offset - {transaction.offset() + 2}, watermark - {self.consumer.table_recovery_status[p]['watermarks'][1]}")
    #                 if self.consumer.table_recovery_status[p]['watermarks'][1] - (transaction.offset() + 2) <= 0:
    #                     LOGGER.info(f'table partition {p} fully recovered!')
    #                     del self.consumer.table_recovery_status[p]
    #             except NoMessageError:
    #                 checks_left -= 1
    #         unassign = {p: p_obj for p, p_obj in self.consumer.pending_recovery_partitions.items() if p not in self.consumer.table_recovery_status}
    #         LOGGER.debug(f'unassigning changelog partitions: {[p for p in unassign]}')
    #         self.consumer.incremental_unassign(list(unassign.values()))
    #         for p in unassign:
    #             del self.consumer.pending_recovery_partitions[p]
    #         # for p_obj in self.consumer.pending_recovery_partitions:
    #         #     del self.consumer.table_recovery_status[p_obj.partition]
    #         LOGGER.info("TABLE RECOVERY COMPLETE!")
    #     LOGGER.debug(f'ASSIGNMENT BEFORE RESUME:\n{[p_obj.partition for p_obj in self.consumer.assignment()]}')
    #     # self.consumer.resume(self.consumer.pending_primary_partitions)
    #     resume = [p_obj for p_obj in self.consumer.assignment() if '__changelog' not in p_obj.topic]
    #     self.consumer.resume(resume)
    #     LOGGER.debug(f'Resuming consumption for partitions:\n{[p_obj.partition for p_obj in resume]}')
    #     LOGGER.info('Continuing normal consumption loop...')
        
    def _table_recovery(self):
        while self.consumer.table_recovery_status:
            # ready_for_seek = False
            try:
                # while not ready_for_seek:
                #     try:
                #         transaction = TableTransaction(self.consume(timeout=2), self.producer, self.consumer,
                #                                        self.metrics_manager,
                #                                        self.changelog_topic)
                #         ready_for_seek = True
                #     except NoMessageError:
                #         LOGGER.debug('waiting for consumer metadata to populate...')
                checks_left = 3
                LOGGER.debug(f'table_recovery_status before recovery attempt: {self.consumer.table_recovery_status}')
                LOGGER.debug(f'pending_recovery_partitions before recovery attempt: {self.consumer.pending_recovery_partitions}')
                seek_list = [p_obj for p, p_obj in self.consumer.pending_recovery_partitions.items() if p in self.consumer.table_recovery_status]
                for p_obj in seek_list:
                    self.consumer.seek(p_obj)
                if self.consumer.table_recovery_status:
                    LOGGER.info('BEGINNING TABLE RECOVERY PROCEDURE')
                    while checks_left:
                        try:
                            transaction = TableTransaction(self.consume(timeout=3), self.producer, self.consumer, self.metrics_manager,
                                                           self.changelog_topic)
                            LOGGER.debug(f'Recovery write is {transaction.value()}')
                            transaction._recover_table_via_changelog()
                            p = transaction.partition()
                            LOGGER.debug(f"transaction_offset - {transaction.offset() + 2}, watermark - {self.consumer.table_recovery_status[p]['watermarks'][1]}")
                            if self.consumer.table_recovery_status[p]['watermarks'][1] - (transaction.offset() + 2) <= 0:
                                LOGGER.info(f'table partition {p} fully recovered!')
                        except NoMessageError:
                            checks_left -= 1
                            LOGGER.debug(f'No changelog messages, checks remaining: {checks_left}')
                    LOGGER.info("TABLE RECOVERY COMPLETE!")
                    LOGGER.debug(f'unassigning changelog partitions: {[p for p in self.consumer.pending_recovery_partitions]}')
                    self.consumer.incremental_unassign(list(self.consumer.pending_recovery_partitions.values()))
                LOGGER.debug(f'ASSIGNMENT BEFORE RESUME:\n{set([(p_obj.topic, p_obj.partition) for p_obj in self.consumer.assignment()])}')
                self.consumer.pending_recovery_partitions = {}
                self.consumer.table_recovery_status = {}
                # resume = [p_obj for p_obj in self.consumer.assignment() if '__changelog' not in p_obj.topic]
                # self.consumer.resume(resume)
                # LOGGER.debug(f'Resuming consumption for partitions:\n{[p_obj.partition for p_obj in resume]}')
                LOGGER.debug(f'Resuming consumption for partitions:\n{set([p_obj.partition for p_obj in self.consumer.pending_primary_partitions])}')
                self.consumer.resume(self.consumer.pending_primary_partitions)
                LOGGER.info('Continuing normal consumption loop...')
                self.consumer.pending_primary_partitions = []
            except Exception as e:
                LOGGER.debug(f'{[arg for arg in e.args]}')
                LOGGER.debug('Table recovery interrupted due to rebalance...retrying')

    
    def run(self, *args, **kwargs):
        transaction = None
        try:
            while True:
                try:
                    transaction = TableTransaction(self.consume(), self.producer, self.consumer, self.metrics_manager, self.changelog_topic)
                    self.app_function(transaction, *args, **kwargs)
                    if not transaction._committed:
                        transaction.commit()
                except NoMessageError:
                    self.producer.poll(0)
                    LOGGER.debug('No messages!')
                except RunTableRecovery:
                    self._table_recovery()
                except Exception as e:
                    raise
        finally:
            LOGGER.info('App is shutting down...')
            try:
                if transaction._active_transaction:
                    self.producer.abort_transaction(10)
            except:
                pass
            finally:
                shutdown_cleanup(consumer=self.consumer)
                _rdb_close()



# ---------------------------------------------------------
#
# Globally accessed methods necessary for table management
#
# ---------------------------------------------------------


def _rdb_close(partitions=None):
    if not partitions:
        partitions = list(rdb_tables.keys())
    LOGGER.debug(f'RocksDB - closing connections for partitions {partitions}')
    for k in partitions:
        rdb_tables[k].close()
        del rdb_tables[k]
        LOGGER.debug(f'partition {k} RocksDB connection closed.')
    LOGGER.info(f'RocksDB - closed connections for partitions {partitions}')


def _rdb_init(partition):
    rdb_tables[partition] = RDB(f'p{partition}')
    LOGGER.debug(f'RocksDB connection for partition {partition} initialized')


def _rocksdb_assign(consumer, partition_objs):
    LOGGER.info('Rebalance triggered!')
    LOGGER.debug(f'Consumer - Assigning additional partitions: {[p_obj.partition for p_obj in partition_objs]}')
    consumer.pending_primary_partitions += partition_objs
    if partition_objs:
        _init_rdb_tables(consumer.pending_primary_partitions)
        current_changelog_partitions, all_changelog_partitions = _changelog_partition_dict(partition_objs, consumer.pending_primary_partitions, consumer.changelog_topic)
        consumer.table_recovery_status = _table_recovery_offsets(rdb_tables, _get_changelog_highwaters(consumer, all_changelog_partitions))
        consumer.incremental_assign(partition_objs)
        if consumer.table_recovery_status:
            # TODO: This might be able to be managed earlier on as part of the "table recovery" logic.
            consumer.pause(partition_objs)
            LOGGER.info(f'Table recovery required: {consumer.table_recovery_status}')
            consumer.pending_recovery_partitions = {k:v for k,v in all_changelog_partitions.items() if k in consumer.table_recovery_status}
            consumer.incremental_assign(list(_changelog_current_offsets(current_changelog_partitions, consumer.pending_recovery_partitions, consumer.table_recovery_status).values()))
    else:
        all_assignments = consumer.assignment()
        if all_assignments:
            LOGGER.debug('No new/additional partitions assigned.')
            LOGGER.info(f'Resuming current assignment of: {[p_obj.partition for p_obj in all_assignments]}')
        else:
            LOGGER.info('Awaiting partition assignments from broker...')
    LOGGER.info('Consumer - partition assignments complete.')
    if consumer.table_recovery_status:
        # Due to confluent-kafka consumers asynchronous operations, the best way to force a desired
        # control flow within the general app consumer loop is to raise an exception and
        # interrupt whatever the app is currently doing and start recovering.
        raise RunTableRecovery

def _rocksdb_unassign(consumer, partition_objs):
    partitions = [p_obj.partition for p_obj in partition_objs]
    LOGGER.debug(f'Consumer - Unassigning topic {consumer.topic} partitions: {partitions}')
    consumer.incremental_unassign(partition_objs)
    consumer.pending_primary_partitions = [p_obj for p_obj in consumer.pending_primary_partitions if p_obj.partition not in partitions]
    consumer.table_recovery_status = {k:v for k,v in consumer.table_recovery_status.items() if k not in partitions}
    consumer.pending_recovery_partitions = {k:v for k,v in consumer.pending_recovery_partitions.items() if k not in partitions}
    LOGGER.debug(f'pending_primary_partitions after unassignment: {consumer.pending_primary_partitions}')
    LOGGER.debug(f'table_recovery_status after unassignment: {consumer.table_recovery_status}')
    LOGGER.debug(f'pending_recovery_partitions after unassignment: {consumer.pending_recovery_partitions}')
    _rdb_close(partitions)
    LOGGER.info('Consumer - Unassignment request complete.')


def _init_rdb_tables(partition_objs):
    for p in partition_objs:
        partition = p.partition
        if partition not in rdb_tables:
            _rdb_init(partition)


def _changelog_partition_dict(partition_objs, all_partition_objs, changelog_topic):
    return (
        {p_obj.partition: TopicPartition(topic=changelog_topic, partition=p_obj.partition, offset=p_obj.offset) for p_obj in partition_objs},
        {p_obj.partition: TopicPartition(topic=changelog_topic, partition=p_obj.partition, offset=p_obj.offset) for p_obj in all_partition_objs})


def _get_changelog_highwaters(consumer, changelog_partitions):
    return {p: consumer.get_watermark_offsets(p_obj) for p, p_obj in changelog_partitions.items()}


def _table_recovery_offsets(rdb_tables, changelog_watermarks):
    tables_to_recover = {}
    for partition, watermarks in changelog_watermarks.items():
        LOGGER.debug(f'(lowwater, highwater) for changelog p{partition}: {watermarks}')
        table_offset = rdb_tables[partition].read('offset')
        if watermarks[0] != watermarks[1]:
            if table_offset:
                table_offset = int(table_offset)
            else:
                table_offset = 0
            if table_offset < watermarks[1]:
                tables_to_recover[partition] = {'table_offset': table_offset, 'watermarks': watermarks}
    return tables_to_recover


def _changelog_current_offsets(changelog_partitions, all_changelog_partitions, tables_to_recover):
    topic = changelog_partitions[0].topic
    for p, offsets in tables_to_recover.items():
        new_offset = tables_to_recover[p]['table_offset']
        low_mark = tables_to_recover[p]['watermarks'][0]
        if low_mark > new_offset: # handles offsets that have been removed/compacted. Should never happen, but ya know
            LOGGER.info(f'p{p} table has an offset ({new_offset}) less than the changelog lowwater ({low_mark}), likely due to retention settings. Setting {low_mark} as offset start point.')
            new_offset = low_mark
        high_mark = tables_to_recover[p]['watermarks'][1]
        LOGGER.debug(f'p{p} changelog has an offset delta of {high_mark - new_offset}')
        all_changelog_partitions[p].offset = new_offset
    return {k:v for k,v in all_changelog_partitions.items() if k in changelog_partitions}
