﻿'''_2567.py

WormGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2287
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6698
from mastapy.system_model.analyses_and_results.power_flows import _3889
from mastapy.gears.rating.worm import _342
from mastapy.system_model.analyses_and_results.system_deflections import _2568, _2566, _2490
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'WormGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetSystemDeflection',)


class WormGearSetSystemDeflection(_2490.GearSetSystemDeflection):
    '''WormGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2287.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2287.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6698.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6698.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3889.WormGearSetPowerFlow':
        '''WormGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3889.WormGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def rating(self) -> '_342.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_342.WormGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_342.WormGearSetRating':
        '''WormGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_342.WormGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def worm_gears_system_deflection(self) -> 'List[_2568.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'WormGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsSystemDeflection, constructor.new(_2568.WormGearSystemDeflection))
        return value

    @property
    def worm_meshes_system_deflection(self) -> 'List[_2566.WormGearMeshSystemDeflection]':
        '''List[WormGearMeshSystemDeflection]: 'WormMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesSystemDeflection, constructor.new(_2566.WormGearMeshSystemDeflection))
        return value
