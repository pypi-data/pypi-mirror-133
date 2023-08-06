﻿'''_7193.py

MassDiscCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7063
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7240
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'MassDiscCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundAdvancedSystemDeflection',)


class MassDiscCompoundAdvancedSystemDeflection(_7240.VirtualComponentCompoundAdvancedSystemDeflection):
    '''MassDiscCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2198.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_7063.MassDiscAdvancedSystemDeflection]':
        '''List[MassDiscAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_7063.MassDiscAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundAdvancedSystemDeflection]':
        '''List[MassDiscCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7063.MassDiscAdvancedSystemDeflection]':
        '''List[MassDiscAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_7063.MassDiscAdvancedSystemDeflection))
        return value
