﻿'''_3873.py

StraightBevelGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2283
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6678
from mastapy.gears.rating.straight_bevel import _367
from mastapy.system_model.analyses_and_results.power_flows import _3872, _3871, _3778
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetPowerFlow',)


class StraightBevelGearSetPowerFlow(_3778.BevelGearSetPowerFlow):
    '''StraightBevelGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2283.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2283.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6678.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6678.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def rating(self) -> '_367.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_367.StraightBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_367.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_367.StraightBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def gears_power_flow(self) -> 'List[_3872.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3872.StraightBevelGearPowerFlow))
        return value

    @property
    def straight_bevel_gears_power_flow(self) -> 'List[_3872.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'StraightBevelGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsPowerFlow, constructor.new(_3872.StraightBevelGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3871.StraightBevelGearMeshPowerFlow]':
        '''List[StraightBevelGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3871.StraightBevelGearMeshPowerFlow))
        return value

    @property
    def straight_bevel_meshes_power_flow(self) -> 'List[_3871.StraightBevelGearMeshPowerFlow]':
        '''List[StraightBevelGearMeshPowerFlow]: 'StraightBevelMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesPowerFlow, constructor.new(_3871.StraightBevelGearMeshPowerFlow))
        return value
