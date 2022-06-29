import lib.aiosql as db
from lib import logger

log = logger.logging()


async def insert_room_info(room_rid, room_real_id, room_title, user_name, user_avatar, user_id, user_sec_id, time):
    # 存在房间信息更新 否则新建
    log.debug(f"正在更新或插入房间信息 -> {room_rid}")
    sql = "INSERT INTO `room_info` (`room_rid`, `room_real_id`, `room_title`,`user_name`, `user_avatar`, `user_id`, `user_sec_id`, `time`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s) ON DUPLICATE KEY UPDATE `room_rid`=%s, `room_real_id`=%s, `room_title`=%s, `user_name`=%s,`user_avatar`=%s, `user_id`=%s, `user_sec_id`=%s, `time`=%s"
    conn = await db.getAmysqlobj()
    await conn.query(sql, (room_rid, room_real_id, room_title, user_name, str(user_avatar), user_id, user_sec_id, time, room_rid, room_real_id, room_title, user_name, str(user_avatar), user_id, user_sec_id, time))
# ON DUPLICATE KEY UPDATE `room_rid`=%s, `room_real_id`=%s, `room_title`=%s, `user_avatar`=%s, `user_id`=%s, `user_sec_id`=%s, `time`=%s


async def insert_room_status(room_id, status, time):
    # 插入新的房间状态
    log.debug(f"正在插入房间状态 -> {room_id}")
    sql = "INSERT INTO `room_status` (`room_id`, `status`, `time`) VALUES (%s, %s, %s);"
    conn = await db.getAmysqlobj()
    await conn.query(sql, (room_id, status, time))


async def insert_room_audience(room_id, total_user, online_user, time):
    # 插入新的直播间人数
    log.debug(f"正在插入直播间人数 -> {room_id}")
    sql = "INSERT INTO `room_audience` (`room_id`, `total_user`, `online_user`,`time`) VALUES(%s, %s, %s,%s);"
    conn = await db.getAmysqlobj()
    await conn.query(sql, (room_id, total_user, online_user, time))


async def query_room_info():  # 查询房间列表
    sql = "SELECT `id`, `room_rid`, `room_real_id` FROM `room_info` ;"
    conn = await db.getAmysqlobj()
    data = await conn.query(sql)
    return data


async def query_data_count():
    sql1 = "SELECT count(*)room_audience FROM `room_audience`"
    sql2 = "SELECT count(*)room_info FROM `room_info`"
    conn = await db.getAmysqlobj()
    data1 = await conn.query(sql1)
    data2 = await conn.query(sql2)
    data = "\n房间在线人数记录总数:"+data1["room_audience"] + \
        "\n"+"受监控的房间数:"+data2["room_info"]+"\n"
    return data
