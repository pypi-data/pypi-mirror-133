'''_4224.py

FaceGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2264
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4222, _4223, _4229
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4084
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'FaceGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundParametricStudyTool',)


class FaceGearSetCompoundParametricStudyTool(_4229.GearSetCompoundParametricStudyTool):
    '''FaceGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2264.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2264.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2264.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2264.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def face_gears_compound_parametric_study_tool(self) -> 'List[_4222.FaceGearCompoundParametricStudyTool]':
        '''List[FaceGearCompoundParametricStudyTool]: 'FaceGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundParametricStudyTool, constructor.new(_4222.FaceGearCompoundParametricStudyTool))
        return value

    @property
    def face_meshes_compound_parametric_study_tool(self) -> 'List[_4223.FaceGearMeshCompoundParametricStudyTool]':
        '''List[FaceGearMeshCompoundParametricStudyTool]: 'FaceMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundParametricStudyTool, constructor.new(_4223.FaceGearMeshCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4084.FaceGearSetParametricStudyTool]':
        '''List[FaceGearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4084.FaceGearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4084.FaceGearSetParametricStudyTool]':
        '''List[FaceGearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4084.FaceGearSetParametricStudyTool))
        return value
