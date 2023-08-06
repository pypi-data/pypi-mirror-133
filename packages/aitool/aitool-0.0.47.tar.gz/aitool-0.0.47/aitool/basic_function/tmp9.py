# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from typing import Dict, Tuple, Union, List, Iterator, Any, NoReturn
import functools
from collections.abc import Iterable
from os import cpu_count
from random import random
from time import sleep, time
from typing import Iterator, Callable, NoReturn

import multiprocess as mp

from time import sleep
from random import random
from aitool import multi


def get_functions(_func: Callable, /, _iter: Iterable) -> Iterable:
    """
    依据一组参数和基础函数，生成一组对应的新函数。
    由于函数的参数结构是：*args, **keywords
    为了方便用户使用，将如下进行参数解析：
    * 如果参数是None，将视为不设置参数
    * 如果参数是不可迭代类型，且不是None，就会被当做*args处理
    * 如果参数是dict类型，就会被当做**keywords处理
    * 如果参数是list类型，就会被当做*arg处理
    * 如果参数是长度为2的tuple类型，就会被当做(*args, **keywords)处理
    * 如果是其他情况会报错

    :param _func: 基础函数
    :param _iter: 一组参数
    :return: 一组对应的新函数
    """
    for condition in _iter:
        if condition is None:
            yield _func
        elif not isinstance(condition, Iterable):
            yield functools.partial(_func, condition)
        elif type(condition) == dict:
            yield functools.partial(_func, **condition)
        elif type(condition) == list:
            yield functools.partial(_func, *condition)
        elif type(condition) == tuple and len(condition) == 2:
            args, keywords = condition
            yield functools.partial(_func, *args, **keywords)
        else:
            # TODO
            # 对condition的解析进行优化，使得能兼容更多数据格式
            raise ValueError(
                """
                Error: 不能识别的参数格式

                由于函数的参数结构是：*args, **keywords
                为了方便用户使用，将如下进行参数解析：
                * 如果参数是不可迭代类型（例如string、int），就会被当做*args处理
                * 如果参数是dict类型，就会被当做**keywords处理
                * 如果参数是list类型，就会被当做*arg处理
                * 如果参数是长度为2的tuple类型，就会被当做(*args, **keywords)处理
                * 如果是其他情况会报错
                """)



def toy(x, y=1):
    return x, y


def bauble(x=1, y=2):
    return x+y


toy_functions = list(get_functions(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]))
bauble_functions = list(get_functions(bauble, [None, -2, [-3], [6, -1], {'y': 4}]))
for result in multi(toy_functions+bauble_functions):
    print(result)