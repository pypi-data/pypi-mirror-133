"""Module init for the python bindings."""

# Copyright 2019 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# pylint: disable=g-multiple-import
# pylint: disable=g-bad-import-order
# pylint: disable=wildcard-import

from . import binding

# Pull some of the native symbols into the public API.
# Hal imports
from .binding import BufferUsage, HalBuffer, HalDevice, HalDriver, HalElementType, MemoryAccess, MemoryType, Shape
# Vm imports
from .binding import create_hal_module, Linkage, VmVariantList, VmFunction, VmInstance, VmContext, VmModule
from .system_api import *
from .function import *
from .tracing import *
