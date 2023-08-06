'''_5658.py

AbstractPeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6608, _6556, _6573, _6582,
    _6583, _6584, _6585, _6586,
    _6604, _6650, _6666, _6693
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    '''AbstractPeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_load_data(self) -> '_6608.HarmonicLoadDataBase':
        '''HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6608.HarmonicLoadDataBase.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to HarmonicLoadDataBase. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6556.ConicalGearSetHarmonicLoadData':
        '''ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6556.ConicalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6573.CylindricalGearSetHarmonicLoadData':
        '''CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6573.CylindricalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6582.ElectricMachineHarmonicLoadData':
        '''ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6582.ElectricMachineHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6583.ElectricMachineHarmonicLoadDataFromExcel':
        '''ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6583.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_flux(self) -> '_6584.ElectricMachineHarmonicLoadDataFromFlux':
        '''ElectricMachineHarmonicLoadDataFromFlux: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6584.ElectricMachineHarmonicLoadDataFromFlux.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromFlux. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6585.ElectricMachineHarmonicLoadDataFromJMAG':
        '''ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6585.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6586.ElectricMachineHarmonicLoadDataFromMotorCAD':
        '''ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6586.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6604.GearSetHarmonicLoadData':
        '''GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6604.GearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6650.PointLoadHarmonicLoadData':
        '''PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6650.PointLoadHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_6666.SpeedDependentHarmonicLoadData':
        '''SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6666.SpeedDependentHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6693.UnbalancedMassHarmonicLoadData':
        '''UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6693.UnbalancedMassHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None
