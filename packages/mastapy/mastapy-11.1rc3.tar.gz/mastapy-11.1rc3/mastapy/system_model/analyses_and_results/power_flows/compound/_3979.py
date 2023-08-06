'''_3979.py

PointLoadCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2207
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3847
from mastapy.system_model.analyses_and_results.power_flows.compound import _4015
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PointLoadCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundPowerFlow',)


class PointLoadCompoundPowerFlow(_4015.VirtualComponentCompoundPowerFlow):
    '''PointLoadCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2207.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2207.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3847.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3847.PointLoadPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3847.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3847.PointLoadPowerFlow))
        return value
