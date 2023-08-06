'''_6831.py

StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2281
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6675
from mastapy.system_model.analyses_and_results.system_deflections import _2544
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6829, _6830, _6741
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation(_6741.BevelGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2281.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6675.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6675.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2544.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2544.StraightBevelDiffGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def straight_bevel_diff_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6829.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6829.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6830.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6830.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
