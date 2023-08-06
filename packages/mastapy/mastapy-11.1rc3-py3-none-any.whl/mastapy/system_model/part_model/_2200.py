'''_2200.py

MountableComponent
'''


from typing import Optional

from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _2013, _2003, _2004, _2011,
    _2016, _2017, _2019, _2020,
    _2021, _2022, _2023, _2025,
    _2026, _2027, _2030, _2031,
    _2009, _2002, _2005, _2006,
    _2010, _2018, _2024, _2029,
    _2032
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2047, _2036, _2038, _2040,
    _2042, _2044, _2046, _2048,
    _2050, _2052, _2055, _2056,
    _2057, _2060, _2062, _2064,
    _2066, _2068
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2070, _2071, _2073, _2074,
    _2076, _2077, _2072, _2075,
    _2078
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2080, _2082, _2084, _2086,
    _2088, _2090, _2091, _2079,
    _2081, _2083, _2085, _2087,
    _2089
)
from mastapy.system_model.part_model import _2173, _2182, _2181
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.part_model.cycloidal import _2304
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponent',)


class MountableComponent(_2181.Component):
    '''MountableComponent

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotation_about_axis(self) -> 'float':
        '''float: 'RotationAboutAxis' is the original name of this property.'''

        return self.wrapped.RotationAboutAxis

    @rotation_about_axis.setter
    def rotation_about_axis(self, value: 'float'):
        self.wrapped.RotationAboutAxis = float(value) if value else 0.0

    @property
    def inner_socket(self) -> '_2013.CylindricalSocket':
        '''CylindricalSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CylindricalSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_bearing_inner_socket(self) -> '_2003.BearingInnerSocket':
        '''BearingInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.BearingInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_bearing_outer_socket(self) -> '_2004.BearingOuterSocket':
        '''BearingOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.BearingOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cvt_pulley_socket(self) -> '_2011.CVTPulleySocket':
        '''CVTPulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.CVTPulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_inner_shaft_socket(self) -> '_2016.InnerShaftSocket':
        '''InnerShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.InnerShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_inner_shaft_socket_base(self) -> '_2017.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.InnerShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_inner_socket(self) -> '_2019.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.MountableComponentInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_outer_socket(self) -> '_2020.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.MountableComponentOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_socket(self) -> '_2021.MountableComponentSocket':
        '''MountableComponentSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.MountableComponentSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_outer_shaft_socket(self) -> '_2022.OuterShaftSocket':
        '''OuterShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.OuterShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_outer_shaft_socket_base(self) -> '_2023.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.OuterShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_planetary_socket(self) -> '_2025.PlanetarySocket':
        '''PlanetarySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.PlanetarySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_planetary_socket_base(self) -> '_2026.PlanetarySocketBase':
        '''PlanetarySocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.PlanetarySocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_pulley_socket(self) -> '_2027.PulleySocket':
        '''PulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.PulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_rolling_ring_socket(self) -> '_2030.RollingRingSocket':
        '''RollingRingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.RollingRingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_shaft_socket(self) -> '_2031.ShaftSocket':
        '''ShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.ShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2047.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.CylindricalGearTeethSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2070.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2071.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2073.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.CycloidalDiscInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2074.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.CycloidalDiscOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2076.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_ring_pins_socket(self) -> '_2077.RingPinsSocket':
        '''RingPinsSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.RingPinsSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_clutch_socket(self) -> '_2080.ClutchSocket':
        '''ClutchSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.ClutchSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_concept_coupling_socket(self) -> '_2082.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_coupling_socket(self) -> '_2084.CouplingSocket':
        '''CouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.CouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2086.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.PartToPartShearCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_spring_damper_socket(self) -> '_2088.SpringDamperSocket':
        '''SpringDamperSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.SpringDamperSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_torque_converter_pump_socket(self) -> '_2090.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.TorqueConverterPumpSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_torque_converter_turbine_socket(self) -> '_2091.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.TorqueConverterTurbineSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_connection(self) -> '_2009.Connection':
        '''Connection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.Connection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to Connection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2002.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_belt_connection(self) -> '_2005.BeltConnection':
        '''BeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.BeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_coaxial_connection(self) -> '_2006.CoaxialConnection':
        '''CoaxialConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.CoaxialConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cvt_belt_connection(self) -> '_2010.CVTBeltConnection':
        '''CVTBeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.CVTBeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_inter_mountable_component_connection(self) -> '_2018.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.InterMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_planetary_connection(self) -> '_2024.PlanetaryConnection':
        '''PlanetaryConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.PlanetaryConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_rolling_ring_connection(self) -> '_2029.RollingRingConnection':
        '''RollingRingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.RollingRingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2032.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.ShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2036.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2036.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_bevel_differential_gear_mesh(self) -> '_2038.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.BevelDifferentialGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_bevel_gear_mesh(self) -> '_2040.BevelGearMesh':
        '''BevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.BevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_concept_gear_mesh(self) -> '_2042.ConceptGearMesh':
        '''ConceptGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.ConceptGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_conical_gear_mesh(self) -> '_2044.ConicalGearMesh':
        '''ConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.ConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cylindrical_gear_mesh(self) -> '_2046.CylindricalGearMesh':
        '''CylindricalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.CylindricalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_face_gear_mesh(self) -> '_2048.FaceGearMesh':
        '''FaceGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.FaceGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_gear_mesh(self) -> '_2050.GearMesh':
        '''GearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.GearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to GearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_hypoid_gear_mesh(self) -> '_2052.HypoidGearMesh':
        '''HypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.HypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2055.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2056.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2057.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2060.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2062.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.StraightBevelDiffGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_straight_bevel_gear_mesh(self) -> '_2064.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.StraightBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_worm_gear_mesh(self) -> '_2066.WormGearMesh':
        '''WormGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.WormGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2068.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.ZerolBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2072.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2075.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_ring_pins_to_disc_connection(self) -> '_2078.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.RingPinsToDiscConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_clutch_connection(self) -> '_2079.ClutchConnection':
        '''ClutchConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.ClutchConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_concept_coupling_connection(self) -> '_2081.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.ConceptCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_coupling_connection(self) -> '_2083.CouplingConnection':
        '''CouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.CouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2085.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.PartToPartShearCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_spring_damper_connection(self) -> '_2087.SpringDamperConnection':
        '''SpringDamperConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2087.SpringDamperConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_torque_converter_connection(self) -> '_2089.TorqueConverterConnection':
        '''TorqueConverterConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.TorqueConverterConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def is_mounted(self) -> 'bool':
        '''bool: 'IsMounted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsMounted

    @property
    def inner_component(self) -> '_2173.AbstractShaft':
        '''AbstractShaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.AbstractShaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to AbstractShaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    @property
    def inner_component_of_type_shaft(self) -> '_2218.Shaft':
        '''Shaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.Shaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to Shaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    @property
    def inner_component_of_type_cycloidal_disc(self) -> '_2304.CycloidalDisc':
        '''CycloidalDisc: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.CycloidalDisc.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    def try_mount_on(self, shaft: '_2173.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2182.ComponentsConnectedResult':
        ''' 'TryMountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryMountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def mount_on(self, shaft: '_2173.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2006.CoaxialConnection':
        ''' 'MountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.CoaxialConnection
        '''

        offset = float(offset)
        method_result = self.wrapped.MountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
