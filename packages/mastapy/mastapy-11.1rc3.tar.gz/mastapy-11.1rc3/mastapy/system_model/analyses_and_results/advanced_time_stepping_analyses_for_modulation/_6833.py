﻿'''_6833.py

StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets.gears import _2064
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.system_model.analyses_and_results.system_deflections import _2546
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6740
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation(_6740.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2064.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6677.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6677.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2546.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2546.StraightBevelGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
