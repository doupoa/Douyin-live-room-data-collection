import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from lib.aiosql import Pmysql
from lib import logger
from utils import req
import config


app = FastAPI()
scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
log = logger.logging()

@app.on_event("startup")
async def startup_event():
    mysqlobj = Pmysql()
    log.info("正在进行数据库连通性测试..")
    await mysqlobj.connect_test()  # 数据库测试
    log.info("数据库连通性测试通过！")
    try:
        cd = int(config.req_cd)
    except:
        log.warn("请求冷却配置错误，已使用默认30秒")
        cd = 30
    for i in config.room_id:
        scheduler.add_job(req.doGet, "interval",
                          seconds=cd, args=[i], coalesce=True, id=i, replace_existing=True)
    scheduler.start()
    log.info(f"定时任务已启动,查询冷却时长{cd}秒")


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.remove_all_jobs()
    scheduler.shutdown(True)


@app.get("/")
async def root():
    return await req.get_data()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8880)
