﻿'''_4556.py

ZerolBevelGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2289
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4554, _4555, _4446
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4427
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ZerolBevelGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundModalAnalysisAtAStiffness',)


class ZerolBevelGearSetCompoundModalAnalysisAtAStiffness(_4446.BevelGearSetCompoundModalAnalysisAtAStiffness):
    '''ZerolBevelGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2289.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2289.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def zerol_bevel_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4554.ZerolBevelGearCompoundModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearCompoundModalAnalysisAtAStiffness]: 'ZerolBevelGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundModalAnalysisAtAStiffness, constructor.new(_4554.ZerolBevelGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4555.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness]: 'ZerolBevelMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_4555.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4427.ZerolBevelGearSetModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetModalAnalysisAtAStiffness]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4427.ZerolBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4427.ZerolBevelGearSetModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetModalAnalysisAtAStiffness]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4427.ZerolBevelGearSetModalAnalysisAtAStiffness))
        return value
