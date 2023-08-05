from .base_pipeline import BasePipeline
from scrapy.exceptions import NotConfigured, NotSupported
import logging

class SimpleMysqlPipeline(BasePipeline):
    """
    简易MysqlPipeline实现
    """
    def __init__(self, settings=None):
        super().__init__(settings)
        mysql_host = settings.get('MYSQL_HOST') or 'localhost'
        mysql_port = settings.get('MYSQL_PORT') or 3306
        mysql_user = settings.get('MYSQL_USERNAME')
        mysql_password = settings.get('MYSQL_PASSWORD')
        mysql_database = settings.get('MYSQL_DATABASE')
        mysql_charset = settings.get('MYSQL_CHARSET') or ''
        self.table = settings.get('MYSQL_TABLE')
        self.logger = logging.getLogger("scrapy_exts.pipelines.SimpleMysqlPipeline")

        try:
            from pyeasytd.mysql_util import MysqlUtil
            self.mysql_ = MysqlUtil.connect(mysql_host, int(mysql_port), mysql_user,
                                            mysql_password, mysql_database)
        except:
            pass

        try:
            import pymysql
        except:
            raise NotSupported

        try:
            self.mysql = pymysql.connect(
                host=mysql_host,
                port=int(mysql_port),
                user=mysql_user,
                password=mysql_password,
                database=mysql_database,
                charset=mysql_charset,
            )
        except:
            self.logger.debug('[WARNING] Not found %s config in settings. Pipeline will not be started.' % 'mysql')
            raise NotConfigured

    def process_item(self, item, spider):
        if self.table:
            if self.mysql_:
                self.mysql_.insert_dict(self.table, dict(item))
            else:
                columns = item.keys()
                sql_str = f'INSERT INTO {self.table}({",".join(columns)}) VALUES ({",".join(["%s" for _ in columns])});'
                cursor = self.mysql.cursor()
                cursor.execute(sql_str, list(item.values()))
                self.mysql.commit()
                cursor.close()

        return item

