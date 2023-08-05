# Copyright 2021 Ross Wightman and Zilliz. All rights reserved.  #
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

import torch
from torch import nn

def tanh(x: torch.Tensor, inplace: bool = False) -> torch.Tensor:
    return x.tanh_() if inplace else x.tanh()

class Tanh(nn.Module):
    """
    Tanh activiation layer.

    A layer applies a tangnet function to the input.

    Args:
        inplace(`Bool`):
            whether use inplace version.
    Returns:
        (`torch.Tensor`)
            output tensor after activation.
    """
    def __init__(self, inplace: bool = False) -> None:
        super().__init__()
        self.inplace = inplace

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.tanh_() if self.inplace else x.tanh()
