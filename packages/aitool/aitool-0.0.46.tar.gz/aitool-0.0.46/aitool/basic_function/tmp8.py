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

# TODO

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
from os import cpu_count
from random import random
from time import sleep
import multiprocess as mp
from aitool import pool_map, pool_starmap, multi_map, exe_time


SLEEP_TIME = [random() for _ in range(10000)]


def toy(x):
    sleep(x)
    return x


def do_something_in_parent_process(data):
    print(data)


@exe_time(print_time=True)
def test_sequence():
    data = [toy(time) for time in SLEEP_TIME]
    do_something_in_parent_process(data)


@exe_time(print_time=True)
def test_use_multi(ordered=False):
    functions = list(get_functions(toy, SLEEP_TIME))
    data = [result for result in multi(functions, ordered=ordered)]
    do_something_in_parent_process(data)


@exe_time(print_time=True)
def test_use_multi(ordered=False):
    functions = list(get_functions(toy, SLEEP_TIME))
    data = [result for result in multi(functions, ordered=ordered)]
    do_something_in_parent_process(data)



@exe_time(print_time=True)
def test_use_multi(ordered=False):
    functions = list(get_functions(toy, SLEEP_TIME))
    data = [result for result in multi(functions, ordered=ordered)]
    do_something_in_parent_process(data)


print(sum(SLEEP_TIME))
test_use_pool()
test_use_multi()
test_use_multi(ordered=True)
test_sequence()
