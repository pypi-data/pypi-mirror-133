'''_2370.py

ModalAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses import _2361
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3283
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _2365
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4350
from mastapy.system_model.analyses_and_results.modal_analyses import _2364, _4896, _4894
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2363
from mastapy.system_model.analyses_and_results.analysis_cases import _7262
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysis',)


class ModalAnalysis(_7262.StaticLoadAnalysisCase):
    '''ModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analysis_results(self) -> '_2361.DynamicAnalysis':
        '''DynamicAnalysis: 'ModalAnalysisResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2361.DynamicAnalysis.TYPE not in self.wrapped.ModalAnalysisResults.__class__.__mro__:
            raise CastException('Failed to cast modal_analysis_results to DynamicAnalysis. Expected: {}.'.format(self.wrapped.ModalAnalysisResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ModalAnalysisResults.__class__)(self.wrapped.ModalAnalysisResults) if self.wrapped.ModalAnalysisResults is not None else None

    @property
    def analysis_settings(self) -> '_4896.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4896.ModalAnalysisOptions)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings is not None else None

    @property
    def bar_model_export(self) -> '_4894.ModalAnalysisBarModelFEExportOptions':
        '''ModalAnalysisBarModelFEExportOptions: 'BarModelExport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4894.ModalAnalysisBarModelFEExportOptions)(self.wrapped.BarModelExport) if self.wrapped.BarModelExport is not None else None
