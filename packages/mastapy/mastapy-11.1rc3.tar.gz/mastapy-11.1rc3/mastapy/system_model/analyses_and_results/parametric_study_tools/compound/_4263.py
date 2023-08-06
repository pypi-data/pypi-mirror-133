'''_4263.py

RootAssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _4116, _4115, _4134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5379, _5378, _5380, _5383,
    _5384, _5387, _5391
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2633
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4176
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'RootAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundParametricStudyTool',)


class RootAssemblyCompoundParametricStudyTool(_4176.AssemblyCompoundParametricStudyTool):
    '''RootAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def results_for_reporting(self) -> '_4116.ParametricStudyToolResultsForReporting':
        '''ParametricStudyToolResultsForReporting: 'ResultsForReporting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4116.ParametricStudyToolResultsForReporting)(self.wrapped.ResultsForReporting) if self.wrapped.ResultsForReporting is not None else None

    @property
    def parametric_analysis_options(self) -> '_4115.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4115.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions is not None else None

    @property
    def compound_load_case(self) -> '_5379.AbstractLoadCaseGroup':
        '''AbstractLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5379.AbstractLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to AbstractLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_abstract_design_state_load_case_group(self) -> '_5378.AbstractDesignStateLoadCaseGroup':
        '''AbstractDesignStateLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5378.AbstractDesignStateLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to AbstractDesignStateLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_abstract_static_load_case_group(self) -> '_5380.AbstractStaticLoadCaseGroup':
        '''AbstractStaticLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5380.AbstractStaticLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to AbstractStaticLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_design_state(self) -> '_5383.DesignState':
        '''DesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5383.DesignState.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to DesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_duty_cycle(self) -> '_5384.DutyCycle':
        '''DutyCycle: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5384.DutyCycle.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to DutyCycle. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_sub_group_in_single_design_state(self) -> '_5387.SubGroupInSingleDesignState':
        '''SubGroupInSingleDesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5387.SubGroupInSingleDesignState.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to SubGroupInSingleDesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def compound_load_case_of_type_time_series_load_case_group(self) -> '_5391.TimeSeriesLoadCaseGroup':
        '''TimeSeriesLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5391.TimeSeriesLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to TimeSeriesLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CompoundLoadCase.__class__)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase is not None else None

    @property
    def root_assembly_duty_cycle_results(self) -> '_2633.DutyCycleEfficiencyResults':
        '''DutyCycleEfficiencyResults: 'RootAssemblyDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2633.DutyCycleEfficiencyResults)(self.wrapped.RootAssemblyDutyCycleResults) if self.wrapped.RootAssemblyDutyCycleResults is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4134.RootAssemblyParametricStudyTool]':
        '''List[RootAssemblyParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4134.RootAssemblyParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4134.RootAssemblyParametricStudyTool]':
        '''List[RootAssemblyParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4134.RootAssemblyParametricStudyTool))
        return value
