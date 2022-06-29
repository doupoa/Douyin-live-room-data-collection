import aiomysql
import config
from lib import logger

log = logger.logging()


class Pmysql:
    def __init__(self):
        self.__coon = None
        self.__pool = None

    async def connect_test(self):
        await aiomysql.connect(host=config.db_host, user=config.db_user,
                               password=config.db_pwd, db=config.db, port=config.db_port, autocommit=True, cursorclass=aiomysql.cursors.DictCursor)
        return

    async def initpool(self):  # 初始化连接池
        # try:
        if self.__pool:
            return self.__pool
        self.__pool = await aiomysql.create_pool(
            minsize=3, maxsize=6, host=config.db_host, user=config.db_user, password=config.db_pwd, db=config.db, port=config.db_port, autocommit=True)
        return self.__pool
        # except Exception as e:
        #     log.error(f'数据库连接异常:{e}')
        #     raise Exception("请排除数据库异常后再尝试重启应用！")

    async def getCurosr(self):  # 取游标
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn, cur

    async def query(self, query, param=None):  # 查询
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(query, param)
            return await cur.fetchall()
        except Exception as e:
            log.error(e)
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)


async def getAmysqlobj():  # 取数据库对象
    mysqlobj = Pmysql()
    pool = await mysqlobj.initpool()
    mysqlobj.pool = pool
    return mysqlobj
