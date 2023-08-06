﻿'''_4294.py

WormGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2287
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4292, _4293, _4229
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4165
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'WormGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundParametricStudyTool',)


class WormGearSetCompoundParametricStudyTool(_4229.GearSetCompoundParametricStudyTool):
    '''WormGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2287.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2287.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2287.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2287.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def worm_gears_compound_parametric_study_tool(self) -> 'List[_4292.WormGearCompoundParametricStudyTool]':
        '''List[WormGearCompoundParametricStudyTool]: 'WormGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundParametricStudyTool, constructor.new(_4292.WormGearCompoundParametricStudyTool))
        return value

    @property
    def worm_meshes_compound_parametric_study_tool(self) -> 'List[_4293.WormGearMeshCompoundParametricStudyTool]':
        '''List[WormGearMeshCompoundParametricStudyTool]: 'WormMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundParametricStudyTool, constructor.new(_4293.WormGearMeshCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4165.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4165.WormGearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4165.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4165.WormGearSetParametricStudyTool))
        return value
