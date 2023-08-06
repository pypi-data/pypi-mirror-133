﻿'''_755.py

ManufacturingMachineDatabase
'''


from mastapy.utility.databases import _1591
from mastapy.gears.manufacturing.bevel import _754
from mastapy._internal.python_net import python_net_import

_MANUFACTURING_MACHINE_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ManufacturingMachineDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ManufacturingMachineDatabase',)


class ManufacturingMachineDatabase(_1591.NamedDatabase['_754.ManufacturingMachine']):
    '''ManufacturingMachineDatabase

    This is a mastapy class.
    '''

    TYPE = _MANUFACTURING_MACHINE_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ManufacturingMachineDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
