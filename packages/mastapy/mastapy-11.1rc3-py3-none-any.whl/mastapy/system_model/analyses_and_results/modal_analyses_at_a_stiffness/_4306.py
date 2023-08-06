﻿'''_4306.py

BearingModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2177
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6529
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4334
from mastapy._internal.python_net import python_net_import

_BEARING_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BearingModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingModalAnalysisAtAStiffness',)


class BearingModalAnalysisAtAStiffness(_4334.ConnectorModalAnalysisAtAStiffness):
    '''BearingModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEARING_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2177.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6529.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6529.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def planetaries(self) -> 'List[BearingModalAnalysisAtAStiffness]':
        '''List[BearingModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingModalAnalysisAtAStiffness))
        return value
