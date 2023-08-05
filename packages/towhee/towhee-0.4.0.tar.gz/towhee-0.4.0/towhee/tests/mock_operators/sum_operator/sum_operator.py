# Copyright 2021 Zilliz. All rights reserved.
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


from typing import NamedTuple, List
from towhee.operator import Operator, SharedType


class SumOperator(Operator):
    """
    Flat input list.
    """

    def __init__(self):
        pass

    def __call__(self, inputs: List[NamedTuple('input', [('num', int)])]):
        Outputs = NamedTuple('Outputs', [('sum', int)])
        nums = [item.num for item in inputs]
        output = Outputs(sum(nums))
        return [output, output]

    @property
    def shared_type(self):
        return SharedType.Shareable
