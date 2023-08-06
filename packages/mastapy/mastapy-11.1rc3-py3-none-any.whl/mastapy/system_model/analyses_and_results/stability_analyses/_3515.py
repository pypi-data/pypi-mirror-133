'''_3515.py

ClutchHalfStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2314
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6543
from mastapy.system_model.analyses_and_results.stability_analyses import _3531
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ClutchHalfStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfStabilityAnalysis',)


class ClutchHalfStabilityAnalysis(_3531.CouplingHalfStabilityAnalysis):
    '''ClutchHalfStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2314.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2314.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6543.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6543.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
