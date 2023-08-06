﻿'''_6993.py

BearingAdvancedSystemDeflection
'''


from typing import List

from mastapy.bearings.bearing_results import _1697, _1705, _1708
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1736, _1743, _1751, _1767,
    _1791
)
from mastapy.system_model.part_model import _2177
from mastapy.system_model.analyses_and_results.static_loads import _6529
from mastapy.system_model.analyses_and_results.system_deflections import _2428
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7021
from mastapy._internal.python_net import python_net_import

_BEARING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BearingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingAdvancedSystemDeflection',)


class BearingAdvancedSystemDeflection(_7021.ConnectorAdvancedSystemDeflection):
    '''BearingAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEARING_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle(self) -> '_1697.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'DutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1697.LoadedBearingDutyCycle.TYPE not in self.wrapped.DutyCycle.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle to LoadedBearingDutyCycle. Expected: {}.'.format(self.wrapped.DutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycle.__class__)(self.wrapped.DutyCycle) if self.wrapped.DutyCycle is not None else None

    @property
    def component_design(self) -> '_2177.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6529.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6529.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def planetaries(self) -> 'List[BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2428.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2428.BearingSystemDeflection))
        return value
