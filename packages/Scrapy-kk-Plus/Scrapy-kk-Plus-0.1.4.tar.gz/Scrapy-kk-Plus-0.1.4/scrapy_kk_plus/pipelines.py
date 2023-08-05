import logging

from scrapy_redis import get_redis_from_settings

from scrapy_kk_plus.libs.bloomfilter import BloomFilter
from scrapy_kk_plus.libs.defaults import BLOOMFILTER_BIT, BLOOMFILTER_HASH_NUMBER
from .libs.pipelinesbase import MysqlBasePipeline

logger = logging.getLogger(__name__)


class PermanentFilterPipeline:
    def __init__(self, bf):
        self.bf = bf

    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        key = settings.get("PF_KEY")
        bf = BloomFilter(server, key, bit, hash_number)

        return cls(bf)

    def process_item(self, item, spider):
        try:
            if item['pf_info']:
                self.bf.insert(item['pf_info']['url'])
        except:
            pass



class MysqlInsertPipeline(MysqlBasePipeline):
    def do_mysql(self, cursor, item):
        fields = ','.join(item.keys())
        values = ','.join(('%({})s'.format(k) for k in item.keys()))
        sql = f'insert ignore into {self.table}({fields}) values({values})'
        cursor.execute(sql, item)


class MysqlUpdatePipeline(MysqlBasePipeline):
    def do_mysql(self, cursor, item):
        update_phrase = [f'{name}=%({name})s' for name in item.keys() if name not in self.update_fixed_fields]
        where_phrase = [f'{name}=%({name})s' for name in self.update_fixed_fields]
        update_sql = f'update {self.table} set {",".join(update_phrase)} where {" and ".join(where_phrase)}'
        cursor.execute(update_sql, item)
