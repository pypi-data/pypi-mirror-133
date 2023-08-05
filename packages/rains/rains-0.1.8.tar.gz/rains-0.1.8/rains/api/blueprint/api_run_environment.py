# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

from rains.api.common import RAINS_DB
from rains.api.common import RAINS_SQL
from rains.api.common import URL_PREFIX
from rains.api.common import jsonify
from rains.api.common import Blueprint
from rains.api.common import ServerParameterHandler


# 运行环境接口蓝图
run_environment_blueprint = Blueprint('run_environment', __name__)


@run_environment_blueprint.route(f'{URL_PREFIX}/run_environment/get', methods=['GET'])
def get() -> jsonify:
    """
    [ 查询运行环境 ]

    * NOT MESSAGE

    Returns:
        jsonify: [ 返回前端的 Json 数据结构 ]

    """

    try:
        data = RAINS_DB.lock_read(RAINS_SQL.run_environment.get())[0]

        return ServerParameterHandler.successful({
            'pool_run_state': bool(data[1]),
            'core_sign_count': data[2],
            'task_sign_count': data[3]
        })

    except BaseException as err:
        return ServerParameterHandler.unsuccessful(f'{ err }')
