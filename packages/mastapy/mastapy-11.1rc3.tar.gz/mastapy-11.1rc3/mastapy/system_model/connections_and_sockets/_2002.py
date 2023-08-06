'''_2002.py

AbstractShaftToMountableComponentConnection
'''


from mastapy.system_model.part_model import (
    _2200, _2177, _2184, _2198,
    _2199, _2202, _2205, _2207,
    _2208, _2213, _2215, _2173
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import (
    _2248, _2250, _2252, _2253,
    _2254, _2256, _2258, _2260,
    _2262, _2263, _2265, _2269,
    _2271, _2273, _2275, _2278,
    _2280, _2282, _2284, _2285,
    _2286, _2288
)
from mastapy.system_model.part_model.cycloidal import _2305, _2304
from mastapy.system_model.part_model.couplings import (
    _2314, _2317, _2319, _2322,
    _2324, _2325, _2331, _2333,
    _2336, _2339, _2340, _2341,
    _2343, _2345
)
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.connections_and_sockets import _2009
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnection',)


class AbstractShaftToMountableComponentConnection(_2009.Connection):
    '''AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mountable_component(self) -> '_2200.MountableComponent':
        '''MountableComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.MountableComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MountableComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bearing(self) -> '_2177.Bearing':
        '''Bearing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.Bearing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Bearing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_connector(self) -> '_2184.Connector':
        '''Connector: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2184.Connector.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Connector. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_mass_disc(self) -> '_2198.MassDisc':
        '''MassDisc: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.MassDisc.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MassDisc. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_measurement_component(self) -> '_2199.MeasurementComponent':
        '''MeasurementComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.MeasurementComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_oil_seal(self) -> '_2202.OilSeal':
        '''OilSeal: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2202.OilSeal.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to OilSeal. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_planet_carrier(self) -> '_2205.PlanetCarrier':
        '''PlanetCarrier: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2205.PlanetCarrier.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_point_load(self) -> '_2207.PointLoad':
        '''PointLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.PointLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PointLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_power_load(self) -> '_2208.PowerLoad':
        '''PowerLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.PowerLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PowerLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_unbalanced_mass(self) -> '_2213.UnbalancedMass':
        '''UnbalancedMass: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.UnbalancedMass.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_virtual_component(self) -> '_2215.VirtualComponent':
        '''VirtualComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.VirtualComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to VirtualComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_agma_gleason_conical_gear(self) -> '_2248.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.AGMAGleasonConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_gear(self) -> '_2250.BevelDifferentialGear':
        '''BevelDifferentialGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.BevelDifferentialGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_planet_gear(self) -> '_2252.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.BevelDifferentialPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_sun_gear(self) -> '_2253.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.BevelDifferentialSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_gear(self) -> '_2254.BevelGear':
        '''BevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.BevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_concept_gear(self) -> '_2256.ConceptGear':
        '''ConceptGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.ConceptGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_conical_gear(self) -> '_2258.ConicalGear':
        '''ConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.ConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cylindrical_gear(self) -> '_2260.CylindricalGear':
        '''CylindricalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.CylindricalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cylindrical_planet_gear(self) -> '_2262.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.CylindricalPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_face_gear(self) -> '_2263.FaceGear':
        '''FaceGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.FaceGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to FaceGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_gear(self) -> '_2265.Gear':
        '''Gear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Gear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Gear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_hypoid_gear(self) -> '_2269.HypoidGear':
        '''HypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2269.HypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to HypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2271.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2273.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2275.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2275.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_spiral_bevel_gear(self) -> '_2278.SpiralBevelGear':
        '''SpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2278.SpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_diff_gear(self) -> '_2280.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2280.StraightBevelDiffGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_gear(self) -> '_2282.StraightBevelGear':
        '''StraightBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.StraightBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_planet_gear(self) -> '_2284.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2284.StraightBevelPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_sun_gear(self) -> '_2285.StraightBevelSunGear':
        '''StraightBevelSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.StraightBevelSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_worm_gear(self) -> '_2286.WormGear':
        '''WormGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.WormGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to WormGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_zerol_bevel_gear(self) -> '_2288.ZerolBevelGear':
        '''ZerolBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.ZerolBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_ring_pins(self) -> '_2305.RingPins':
        '''RingPins: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.RingPins.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RingPins. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_clutch_half(self) -> '_2314.ClutchHalf':
        '''ClutchHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.ClutchHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ClutchHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_concept_coupling_half(self) -> '_2317.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.ConceptCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_coupling_half(self) -> '_2319.CouplingHalf':
        '''CouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.CouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cvt_pulley(self) -> '_2322.CVTPulley':
        '''CVTPulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.CVTPulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CVTPulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_part_to_part_shear_coupling_half(self) -> '_2324.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2324.PartToPartShearCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_pulley(self) -> '_2325.Pulley':
        '''Pulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.Pulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Pulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_rolling_ring(self) -> '_2331.RollingRing':
        '''RollingRing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2331.RollingRing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RollingRing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_shaft_hub_connection(self) -> '_2333.ShaftHubConnection':
        '''ShaftHubConnection: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.ShaftHubConnection.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_spring_damper_half(self) -> '_2336.SpringDamperHalf':
        '''SpringDamperHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2336.SpringDamperHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_half(self) -> '_2339.SynchroniserHalf':
        '''SynchroniserHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.SynchroniserHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_part(self) -> '_2340.SynchroniserPart':
        '''SynchroniserPart: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2340.SynchroniserPart.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_sleeve(self) -> '_2341.SynchroniserSleeve':
        '''SynchroniserSleeve: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.SynchroniserSleeve.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_torque_converter_pump(self) -> '_2343.TorqueConverterPump':
        '''TorqueConverterPump: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2343.TorqueConverterPump.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_torque_converter_turbine(self) -> '_2345.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2345.TorqueConverterTurbine.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def shaft(self) -> '_2173.AbstractShaft':
        '''AbstractShaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.AbstractShaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to AbstractShaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None

    @property
    def shaft_of_type_shaft(self) -> '_2218.Shaft':
        '''Shaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.Shaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to Shaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None

    @property
    def shaft_of_type_cycloidal_disc(self) -> '_2304.CycloidalDisc':
        '''CycloidalDisc: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.CycloidalDisc.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to CycloidalDisc. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None
