import json

import httpx
from lib import logger

from utils import sql

online_user = []
online_room = []
ck = None


log = logger.logging()


async def parse(json_data, room_rid):  # 解析数据
    try:
        data = json.loads(json_data)
    except Exception as e:
        log.error(f"[{room_rid}]在解析数据时 -> {e}")
        return
    code = data["status_code"]
    if code != 0:
        log.warn(f"[{room_rid}]数据请求失败，状态码 -> {code}")
        return
    # 基础信息
    live_room_mode = data["data"]["data"][0]["live_room_mode"]  # 房间模式
    room_title = data["data"]["data"][0]["title"]  # 房间名
    room_status = data["data"]["room_status"]  # 房间状态
    status = data["data"]["data"][0]["status"]
    room_id = data["data"]["data"][0]["id_str"]  # 房间真实id
    user_avatar = data["data"]["user"]["avatar_thumb"]["url_list"]  # 头像列表
    user_id = data["data"]["user"]["id_str"]  # 用户id
    user_nickname = data["data"]["user"]["nickname"]  # 用户昵称
    sec_uid = data["data"]["user"]["sec_uid"]  # 用户sec_id
    time_now = data["extra"]["now"]  # 数据时间
    await sql.insert_room_info(room_rid, room_id, room_title,
                               user_nickname, user_avatar, user_id, sec_uid, time_now)  # 更新或插入房间数据
    if status == 2:
        # 观看总人数
        total_user = data["data"]["data"][0]["stats"]["total_user_str"]
        # 当前观看人数
        user_count = data["data"]["data"][0]["stats"]["user_count_str"]
        await sql.insert_room_audience(room_rid, total_user,
                                       user_count, time_now)  # 插入在线人数
        if user_nickname in online_user:
            return
        else:
            await sql.insert_room_status(room_rid, 1, time_now)
            online_user.append(user_nickname)
            online_room.append(room_title)
            log.info(user_nickname + "当前在线")
            log.debug(f"{user_nickname}当前在线 - {room_rid}")
    else:
        if user_nickname in online_user:
            await sql.insert_room_status(room_rid, 0, time_now)
            online_user.remove(user_nickname)
            online_room.remove(room_title)
            log.info(user_nickname+"已离线")
    return


async def get_data():
    room_data = "当前在线:\n"
    for i in range(len(online_user)):
        room_data = room_data + online_user[i] + "的" + online_room[i]+"\n"
    sqldata = await sql.query_data_count()
    room_data = room_data + sqldata
    return room_data


async def doGet(room_rid):  # 执行查询
    global ck
    async with httpx.AsyncClient() as client:
        if ck == None:
            res = await client.get("https://live.douyin.com")
            ck = res.cookies
        url = "https://live.douyin.com/webcast/web/enter/?aid=6383&web_rid="+room_rid
        try:
            res = await client.get(url=url, cookies=ck, timeout=3)
            await parse(res.text, room_rid)
        except Exception as e:
            log.error(f"在请求数据时(room:{room_rid}) -> 连接超时或已断网{e}")
