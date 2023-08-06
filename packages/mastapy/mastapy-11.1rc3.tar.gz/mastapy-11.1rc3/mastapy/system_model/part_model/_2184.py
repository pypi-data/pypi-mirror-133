'''_2184.py

Connector
'''


from typing import Optional

from mastapy.system_model.connections_and_sockets import (
    _2013, _2003, _2004, _2011,
    _2016, _2017, _2019, _2020,
    _2021, _2022, _2023, _2025,
    _2026, _2027, _2030, _2031,
    _2009, _2002, _2005, _2006,
    _2010, _2018, _2024, _2029,
    _2032
)
from mastapy._internal import constructor
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
from mastapy.system_model.part_model import (
    _2173, _2182, _2181, _2200
)
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.part_model.cycloidal import _2304
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2200.MountableComponent):
    '''Connector

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_socket(self) -> '_2013.CylindricalSocket':
        '''CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CylindricalSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_bearing_inner_socket(self) -> '_2003.BearingInnerSocket':
        '''BearingInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.BearingInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_2004.BearingOuterSocket':
        '''BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.BearingOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_2011.CVTPulleySocket':
        '''CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.CVTPulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_2016.InnerShaftSocket':
        '''InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.InnerShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_2017.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.InnerShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_inner_socket(self) -> '_2019.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.MountableComponentInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_outer_socket(self) -> '_2020.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.MountableComponentOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_socket(self) -> '_2021.MountableComponentSocket':
        '''MountableComponentSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.MountableComponentSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_2022.OuterShaftSocket':
        '''OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.OuterShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket_base(self) -> '_2023.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.OuterShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_2025.PlanetarySocket':
        '''PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.PlanetarySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_2026.PlanetarySocketBase':
        '''PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.PlanetarySocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_2027.PulleySocket':
        '''PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.PulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_2030.RollingRingSocket':
        '''RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.RollingRingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_2031.ShaftSocket':
        '''ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.ShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2047.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.CylindricalGearTeethSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2070.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2071.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2073.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.CycloidalDiscInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2074.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.CycloidalDiscOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2076.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_2077.RingPinsSocket':
        '''RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.RingPinsSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_2080.ClutchSocket':
        '''ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.ClutchSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_2082.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_2084.CouplingSocket':
        '''CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.CouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2086.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.PartToPartShearCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2088.SpringDamperSocket':
        '''SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.SpringDamperSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2090.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.TorqueConverterPumpSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2091.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.TorqueConverterTurbineSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_connection(self) -> '_2009.Connection':
        '''Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.Connection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2002.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_2005.BeltConnection':
        '''BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.BeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_2006.CoaxialConnection':
        '''CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.CoaxialConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_2010.CVTBeltConnection':
        '''CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.CVTBeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_2018.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.InterMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_2024.PlanetaryConnection':
        '''PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.PlanetaryConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_2029.RollingRingConnection':
        '''RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.RollingRingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2032.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.ShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2036.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2036.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_2038.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.BevelDifferentialGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_2040.BevelGearMesh':
        '''BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.BevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_2042.ConceptGearMesh':
        '''ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.ConceptGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_2044.ConicalGearMesh':
        '''ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.ConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_2046.CylindricalGearMesh':
        '''CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.CylindricalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_2048.FaceGearMesh':
        '''FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.FaceGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_2050.GearMesh':
        '''GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.GearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_2052.HypoidGearMesh':
        '''HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.HypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2055.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2056.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2057.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2060.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2062.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.StraightBevelDiffGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_2064.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.StraightBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_2066.WormGearMesh':
        '''WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.WormGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2068.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.ZerolBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2072.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2075.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_2078.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.RingPinsToDiscConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_2079.ClutchConnection':
        '''ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.ClutchConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_2081.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.ConceptCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_2083.CouplingConnection':
        '''CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.CouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2085.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.PartToPartShearCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2087.SpringDamperConnection':
        '''SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2087.SpringDamperConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2089.TorqueConverterConnection':
        '''TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.TorqueConverterConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_component(self) -> '_2173.AbstractShaft':
        '''AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.AbstractShaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    @property
    def outer_component_of_type_shaft(self) -> '_2218.Shaft':
        '''Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.Shaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2304.CycloidalDisc':
        '''CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.CycloidalDisc.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    def house_in(self, shaft: '_2173.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2009.Connection':
        ''' 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def try_house_in(self, shaft: '_2173.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2182.ComponentsConnectedResult':
        ''' 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def other_component(self, component: '_2181.Component') -> '_2173.AbstractShaft':
        ''' 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        '''

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
