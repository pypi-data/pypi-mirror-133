import math
from typing import Optional

import jax.random as jrandom

from ..custom_types import Array
from ..module import Module, static_field


class Linear(Module):
    weight: Array
    bias: Optional[Array]
    in_features: int = static_field()
    out_features: int = static_field()
    use_bias: bool = static_field()

    def __init__(self, in_features, out_features, use_bias=True, *, key):
        super().__init__()
        wkey, bkey = jrandom.split(key, 2)
        lim = 1 / math.sqrt(in_features)
        self.weight = jrandom.uniform(
            wkey, (out_features, in_features), minval=-lim, maxval=lim
        )
        if use_bias:
            self.bias = jrandom.uniform(bkey, (out_features,), minval=-lim, maxval=lim)
        else:
            self.bias = None

        self.in_features = in_features
        self.out_features = out_features
        self.use_bias = use_bias

    def __call__(self, x, *, key=None):
        x = self.weight @ x
        if self.bias is not None:
            x = x + self.bias
        return x


class Identity(Module):
    def __init__(self, *args, **kwargs):
        # Ignores args and kwargs
        super().__init__()

    def __call__(self, x, *, key=None):
        return x
