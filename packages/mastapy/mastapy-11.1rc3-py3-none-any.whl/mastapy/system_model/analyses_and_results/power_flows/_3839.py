'''_3839.py

OilSealPowerFlow
'''


from mastapy.system_model.part_model import _2202
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6639
from mastapy.system_model.analyses_and_results.power_flows import _3796
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'OilSealPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealPowerFlow',)


class OilSealPowerFlow(_3796.ConnectorPowerFlow):
    '''OilSealPowerFlow

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2202.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6639.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6639.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
