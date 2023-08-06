﻿'''_1343.py

ParetoOptimisationStrategy
'''


from typing import List

from mastapy.math_utility.optimisation import _1341, _1342, _1345
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1592
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategy',)


class ParetoOptimisationStrategy(_1592.NamedDatabaseItem):
    '''ParetoOptimisationStrategy

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inputs(self) -> 'List[_1341.ParetoOptimisationInput]':
        '''List[ParetoOptimisationInput]: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Inputs, constructor.new(_1341.ParetoOptimisationInput))
        return value

    @property
    def outputs(self) -> 'List[_1342.ParetoOptimisationOutput]':
        '''List[ParetoOptimisationOutput]: 'Outputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Outputs, constructor.new(_1342.ParetoOptimisationOutput))
        return value

    @property
    def charts(self) -> 'List[_1345.ParetoOptimisationStrategyChartInformation]':
        '''List[ParetoOptimisationStrategyChartInformation]: 'Charts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Charts, constructor.new(_1345.ParetoOptimisationStrategyChartInformation))
        return value

    def add_chart(self):
        ''' 'AddChart' is the original name of this method.'''

        self.wrapped.AddChart()
