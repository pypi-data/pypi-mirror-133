﻿'''_6365.py

StraightBevelGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2283
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6678
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6363, _6364, _6271
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'StraightBevelGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCriticalSpeedAnalysis',)


class StraightBevelGearSetCriticalSpeedAnalysis(_6271.BevelGearSetCriticalSpeedAnalysis):
    '''StraightBevelGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCriticalSpeedAnalysis.TYPE'):
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
    def straight_bevel_gears_critical_speed_analysis(self) -> 'List[_6363.StraightBevelGearCriticalSpeedAnalysis]':
        '''List[StraightBevelGearCriticalSpeedAnalysis]: 'StraightBevelGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCriticalSpeedAnalysis, constructor.new(_6363.StraightBevelGearCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_meshes_critical_speed_analysis(self) -> 'List[_6364.StraightBevelGearMeshCriticalSpeedAnalysis]':
        '''List[StraightBevelGearMeshCriticalSpeedAnalysis]: 'StraightBevelMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCriticalSpeedAnalysis, constructor.new(_6364.StraightBevelGearMeshCriticalSpeedAnalysis))
        return value
