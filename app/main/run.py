#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests
import json
requests.packages.urllib3.disable_warnings()

async def get_asset_scope(api, token, search=''):
    logger.info(f"[灯塔助手通知] APP执行参数为: {api} {token} {search}")

    headers = {'accept': 'application/json','Token': token}
    try:
        r = requests.get(
            url=f"https://{api}/api/asset_scope/?{search}",
            headers=headers, 
            verify=False)
    except Exception as e:
        logger.error("[灯塔助手通知] 请求灯塔 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求灯塔资产组 API 失败"}

    return {"status": 0, "result": r.json()}

async def get_asset_scope_site(api, token, scope_id='', site='', search=''):
    logger.info(f"[灯塔助手通知] APP执行参数为: {api} {token}")

    headers = {'accept': 'application/json','Token': token}
    try:
        r = requests.get(
            url=f"https://{api}/api/asset_site/?site={site}&scope_id={scope_id}&{search}",
            headers=headers, 
            verify=False)
    except Exception as e:
        logger.error("[灯塔助手通知] 请求灯塔 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求灯塔资产组站点 API 失败"}

    return {"status": 0, "result": r.json()}

async def add_site_tag(api, token, _id='', tag=''):
    logger.info(f"[灯塔助手通知] APP执行参数为: {api} {token}")

    headers = {'accept': 'application/json','Token': token,'Content-Type':'application/json'}
    try:
        r = requests.post(
            url=f"https://{api}/api/asset_site/add_tag/",
            headers=headers,
            data=json.dumps({"tag": tag,"_id": _id}),
            verify=False)
    except Exception as e:
        logger.error("[灯塔助手通知] 请求灯塔 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求灯塔资产组站点 API 失败"}

    return {"status": 0, "result": r.json()}

if __name__ == '__main__': 
    # 导入异步库
    import asyncio

    # 测试函数
    async def test():
        result = await get_asset_scope_site(api='82.156.212.66:5003', token='ff44256c-fa2b-483f-9956-b0a84e153yjt', search='status=200', scope_id='61c3e272ceacda0012d3a5df')
        print(result)


    # 加入异步队列
    async def main(): await asyncio.gather(test())


    # 启动执行
    asyncio.run(main())