from functools import lru_cache
from typing import Mapping

import torch
from potc.fixture import rule, Addons


@lru_cache()
def _get_dtypes() -> Mapping[torch.dtype, str]:
    dtype_names = filter(lambda x: isinstance(getattr(torch, x), torch.dtype), dir(torch))
    return {getattr(torch, k): k for k in dtype_names}


@rule(type_=torch.dtype)
def torch_dtype(v: torch.dtype, addon: Addons):
    return addon.obj(torch).__getattr__(_get_dtypes()[v])


@rule(type_=torch.Tensor)
def torch_tensor(v: torch.Tensor, addon: Addons):
    return addon.obj(torch).as_tensor(v.numpy().tolist(), dtype=v.dtype)


@rule(type_=torch.Size)
def torch_size(v: torch.Size, addon: Addons):
    return addon.obj(torch).Size(list(v))


@rule(type_=torch.device)
def torch_device(v: torch.device, addon: Addons):
    device_func = addon.obj(torch).device
    if v.index is not None:
        return device_func(v.type, v.index)
    else:
        return device_func(v.type)
