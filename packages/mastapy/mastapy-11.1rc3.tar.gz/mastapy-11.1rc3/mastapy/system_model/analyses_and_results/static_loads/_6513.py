﻿'''_6513.py

LoadCase
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results.rolling import _1814, _1715, _1720
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1854
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _1954, _1951, _1964
from mastapy.gears import _303
from mastapy.system_model.analyses_and_results.static_loads import (
    _6692, _6520, _6652, _6686,
    _6517, _6516, _6518, _6529,
    _6541, _6540, _6546, _6559,
    _6578, _6593, _6597, _6598,
    _6528, _6606, _6633, _6634,
    _6637, _6639, _6641, _6648,
    _6651, _6661, _6665, _6694,
    _6695, _6663, _6550, _6552,
    _6594, _6596, _6523, _6525,
    _6532, _6534, _6535, _6536,
    _6537, _6539, _6553, _6557,
    _6570, _6574, _6575, _6600,
    _6605, _6617, _6619, _6624,
    _6626, _6627, _6629, _6630,
    _6632, _6646, _6667, _6669,
    _6673, _6675, _6676, _6678,
    _6679, _6680, _6696, _6698,
    _6699, _6701, _6566, _6568,
    _6656, _6644, _6643, _6531,
    _6544, _6543, _6549, _6548,
    _6562, _6561, _6564, _6565,
    _6653, _6662, _6660, _6658,
    _6672, _6671, _6682, _6681,
    _6683, _6684, _6687, _6688,
    _6689, _6664, _6563, _6530,
    _6545, _6558, _6623, _6645,
    _6659, _6519, _6533, _6551,
    _6595, _6674, _6538, _6555,
    _6524, _6572, _6618, _6625,
    _6628, _6631, _6668, _6677,
    _6697, _6700, _6602, _6567,
    _6569, _6657, _6642, _6542,
    _6547, _6560, _6670
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4115
from mastapy.system_model.connections_and_sockets.couplings import (
    _2089, _2085, _2079, _2081,
    _2083, _2087
)
from mastapy.system_model.part_model import (
    _2173, _2172, _2174, _2177,
    _2179, _2180, _2181, _2184,
    _2185, _2188, _2189, _2190,
    _2171, _2191, _2198, _2199,
    _2200, _2202, _2204, _2205,
    _2207, _2208, _2210, _2212,
    _2213, _2215
)
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.part_model.gears import (
    _2256, _2257, _2263, _2264,
    _2248, _2249, _2250, _2251,
    _2252, _2253, _2254, _2255,
    _2258, _2259, _2260, _2261,
    _2262, _2265, _2267, _2269,
    _2270, _2271, _2272, _2273,
    _2274, _2275, _2276, _2277,
    _2278, _2279, _2280, _2281,
    _2282, _2283, _2284, _2285,
    _2286, _2287, _2288, _2289
)
from mastapy.system_model.part_model.cycloidal import _2303, _2304, _2305
from mastapy.system_model.part_model.couplings import (
    _2323, _2324, _2311, _2313,
    _2314, _2316, _2317, _2318,
    _2319, _2321, _2322, _2325,
    _2333, _2331, _2332, _2335,
    _2336, _2337, _2339, _2340,
    _2341, _2342, _2343, _2345
)
from mastapy.system_model.connections_and_sockets import (
    _2032, _2010, _2005, _2006,
    _2009, _2018, _2024, _2029,
    _2002
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2038, _2042, _2048, _2062,
    _2040, _2044, _2036, _2046,
    _2052, _2055, _2056, _2057,
    _2060, _2064, _2066, _2068,
    _2050
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2072, _2075, _2078
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2385

_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2385.Context):
    '''LoadCase

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugal

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugalRingExpansion

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def use_node_per_bearing_row_inner(self) -> 'bool':
        '''bool: 'UseNodePerBearingRowInner' is the original name of this property.'''

        return self.wrapped.UseNodePerBearingRowInner

    @use_node_per_bearing_row_inner.setter
    def use_node_per_bearing_row_inner(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowInner = bool(value) if value else False

    @property
    def use_node_per_bearing_row_outer(self) -> 'bool':
        '''bool: 'UseNodePerBearingRowOuter' is the original name of this property.'''

        return self.wrapped.UseNodePerBearingRowOuter

    @use_node_per_bearing_row_outer.setter
    def use_node_per_bearing_row_outer(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowOuter = bool(value) if value else False

    @property
    def roller_analysis_method(self) -> '_1814.RollerAnalysisMethod':
        '''RollerAnalysisMethod: 'RollerAnalysisMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RollerAnalysisMethod)
        return constructor.new(_1814.RollerAnalysisMethod)(value) if value is not None else None

    @roller_analysis_method.setter
    def roller_analysis_method(self, value: '_1814.RollerAnalysisMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RollerAnalysisMethod = value

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        '''bool: 'IncludePlanetaryCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludePlanetaryCentrifugal

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        '''bool: 'IncludeGravity' is the original name of this property.'''

        return self.wrapped.IncludeGravity

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.StressConcentrationMethodForRating, value) if self.wrapped.StressConcentrationMethodForRating is not None else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfStripsForRollerCalculation) if self.wrapped.NumberOfStripsForRollerCalculation is not None else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def use_default_temperatures(self) -> 'bool':
        '''bool: 'UseDefaultTemperatures' is the original name of this property.'''

        return self.wrapped.UseDefaultTemperatures

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        '''bool: 'IncludeFittingEffects' is the original name of this property.'''

        return self.wrapped.IncludeFittingEffects

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        '''bool: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        return self.wrapped.IncludeThermalExpansionEffects

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def expand_grounded_nodes_for_thermal_effects(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'ExpandGroundedNodesForThermalEffects' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.ExpandGroundedNodesForThermalEffects) if self.wrapped.ExpandGroundedNodesForThermalEffects is not None else None

    @expand_grounded_nodes_for_thermal_effects.setter
    def expand_grounded_nodes_for_thermal_effects(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.ExpandGroundedNodesForThermalEffects = value

    @property
    def include_ring_ovality(self) -> 'bool':
        '''bool: 'IncludeRingOvality' is the original name of this property.'''

        return self.wrapped.IncludeRingOvality

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def ring_ovality_scaling(self) -> 'float':
        '''float: 'RingOvalityScaling' is the original name of this property.'''

        return self.wrapped.RingOvalityScaling

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        '''bool: 'IncludeGearBlankElasticDistortion' is the original name of this property.'''

        return self.wrapped.IncludeGearBlankElasticDistortion

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        '''bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property.'''

        return self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def ball_bearing_contact_calculation(self) -> '_1715.BallBearingContactCalculation':
        '''BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BallBearingContactCalculation)
        return constructor.new(_1715.BallBearingContactCalculation)(value) if value is not None else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1715.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        '''bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return self.wrapped.ModelBearingMountingClearancesAutomatically

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment':
        '''enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment: 'BallBearingFrictionModelForGyroscopicMoment' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.BallBearingFrictionModelForGyroscopicMoment, value) if self.wrapped.BallBearingFrictionModelForGyroscopicMoment is not None else None

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    def ball_bearing_friction_model_for_gyroscopic_moment(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BallBearingFrictionModelForGyroscopicMoment = value

    @property
    def include_rib_contact_analysis(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'IncludeRibContactAnalysis' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.IncludeRibContactAnalysis) if self.wrapped.IncludeRibContactAnalysis is not None else None

    @include_rib_contact_analysis.setter
    def include_rib_contact_analysis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.IncludeRibContactAnalysis = value

    @property
    def number_of_grid_points_across_rib_height(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfGridPointsAcrossRibHeight' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfGridPointsAcrossRibHeight) if self.wrapped.NumberOfGridPointsAcrossRibHeight is not None else None

    @number_of_grid_points_across_rib_height.setter
    def number_of_grid_points_across_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibHeight = value

    @property
    def number_of_grid_points_across_rib_contact_width(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfGridPointsAcrossRibContactWidth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfGridPointsAcrossRibContactWidth) if self.wrapped.NumberOfGridPointsAcrossRibContactWidth is not None else None

    @number_of_grid_points_across_rib_contact_width.setter
    def number_of_grid_points_across_rib_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibContactWidth = value

    @property
    def refine_grid_around_contact_point(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'RefineGridAroundContactPoint' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.RefineGridAroundContactPoint) if self.wrapped.RefineGridAroundContactPoint is not None else None

    @refine_grid_around_contact_point.setter
    def refine_grid_around_contact_point(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.RefineGridAroundContactPoint = value

    @property
    def grid_refinement_factor_rib_height(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'GridRefinementFactorRibHeight' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.GridRefinementFactorRibHeight) if self.wrapped.GridRefinementFactorRibHeight is not None else None

    @grid_refinement_factor_rib_height.setter
    def grid_refinement_factor_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorRibHeight = value

    @property
    def grid_refinement_factor_contact_width(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'GridRefinementFactorContactWidth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.GridRefinementFactorContactWidth) if self.wrapped.GridRefinementFactorContactWidth is not None else None

    @grid_refinement_factor_contact_width.setter
    def grid_refinement_factor_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorContactWidth = value

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionLengthToDiameterRatio

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        '''bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForCylindricalGearMeshes

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        '''int: 'MinimumNumberOfGearMeshNodes' is the original name of this property.'''

        return self.wrapped.MinimumNumberOfGearMeshNodes

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        '''float: 'PeakLoadFactorForShafts' is the original name of this property.'''

        return self.wrapped.PeakLoadFactorForShafts

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MeshStiffnessModel, value) if self.wrapped.MeshStiffnessModel is not None else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        '''overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property.'''

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MicroGeometryModelInSystemDeflection, value) if self.wrapped.MicroGeometryModelInSystemDeflection is not None else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded is not None else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded is not None else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EnergyConvergenceAbsoluteTolerance) if self.wrapped.EnergyConvergenceAbsoluteTolerance is not None else None

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_1951.HypoidWindUpRemovalMethod':
        '''HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments)
        return constructor.new(_1951.HypoidWindUpRemovalMethod)(value) if value is not None else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_1951.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        '''bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property.'''

        return self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumPowerForGearMeshToBeLoaded) if self.wrapped.MinimumPowerForGearMeshToBeLoaded is not None else None

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumTorqueForGearMeshToBeLoaded) if self.wrapped.MinimumTorqueForGearMeshToBeLoaded is not None else None

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        '''float: 'ToleranceFactorForOuterFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForOuterFit

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        '''float: 'ToleranceFactorForInnerFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForInnerFit

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterSupport) if self.wrapped.ToleranceFactorForOuterSupport is not None else None

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterRing) if self.wrapped.ToleranceFactorForOuterRing is not None else None

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerSupport) if self.wrapped.ToleranceFactorForInnerSupport is not None else None

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerRing) if self.wrapped.ToleranceFactorForInnerRing is not None else None

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveBore) if self.wrapped.ToleranceFactorForInnerMountingSleeveBore is not None else None

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    def tolerance_factor_for_inner_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveBore = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter is not None else None

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveBore) if self.wrapped.ToleranceFactorForOuterMountingSleeveBore is not None else None

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    def tolerance_factor_for_outer_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveBore = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter is not None else None

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForRadialInternalClearances

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForAxialInternalClearances

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RelativeToleranceForConvergence) if self.wrapped.RelativeToleranceForConvergence is not None else None

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AirDensity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AirDensity) if self.wrapped.AirDensity is not None else None

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AirDensity = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedOfSound' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedOfSound) if self.wrapped.SpeedOfSound is not None else None

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpeedOfSound = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CharacteristicSpecificAcousticImpedance) if self.wrapped.CharacteristicSpecificAcousticImpedance is not None else None

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self) -> 'bool':
        '''bool: 'IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis' is the original name of this property.'''

        return self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis

    @include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis.setter
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self, value: 'bool'):
        self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis = bool(value) if value else False

    @property
    def transmission_efficiency_settings(self) -> '_6692.TransmissionEfficiencySettings':
        '''TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6692.TransmissionEfficiencySettings)(self.wrapped.TransmissionEfficiencySettings) if self.wrapped.TransmissionEfficiencySettings is not None else None

    @property
    def additional_acceleration(self) -> '_6520.AdditionalAccelerationOptions':
        '''AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6520.AdditionalAccelerationOptions)(self.wrapped.AdditionalAcceleration) if self.wrapped.AdditionalAcceleration is not None else None

    @property
    def temperatures(self) -> '_1964.TransmissionTemperatureSet':
        '''TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.TransmissionTemperatureSet)(self.wrapped.Temperatures) if self.wrapped.Temperatures is not None else None

    @property
    def input_power_load(self) -> '_6652.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6652.PowerLoadLoadCase)(self.wrapped.InputPowerLoad) if self.wrapped.InputPowerLoad is not None else None

    @property
    def output_power_load(self) -> '_6652.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6652.PowerLoadLoadCase)(self.wrapped.OutputPowerLoad) if self.wrapped.OutputPowerLoad is not None else None

    @property
    def parametric_study_tool_options(self) -> '_4115.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4115.ParametricStudyToolOptions)(self.wrapped.ParametricStudyToolOptions) if self.wrapped.ParametricStudyToolOptions is not None else None

    @property
    def power_loads(self) -> 'List[_6652.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6652.PowerLoadLoadCase))
        return value

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def inputs_for_torque_converter_connection(self, design_entity: '_2089.TorqueConverterConnection') -> '_6686.TorqueConverterConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft(self, design_entity: '_2173.AbstractShaft') -> '_6517.AbstractShaftLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_abstract_assembly(self, design_entity: '_2172.AbstractAssembly') -> '_6516.AbstractAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_2174.AbstractShaftOrHousing') -> '_6518.AbstractShaftOrHousingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bearing(self, design_entity: '_2177.Bearing') -> '_6529.BearingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bolt(self, design_entity: '_2179.Bolt') -> '_6541.BoltLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bolted_joint(self, design_entity: '_2180.BoltedJoint') -> '_6540.BoltedJointLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_component(self, design_entity: '_2181.Component') -> '_6546.ComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_connector(self, design_entity: '_2184.Connector') -> '_6559.ConnectorLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_datum(self, design_entity: '_2185.Datum') -> '_6578.DatumLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_external_cad_model(self, design_entity: '_2188.ExternalCADModel') -> '_6593.ExternalCADModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_fe_part(self, design_entity: '_2189.FEPart') -> '_6597.FEPartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_2190.FlexiblePinAssembly') -> '_6598.FlexiblePinAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_assembly(self, design_entity: '_2171.Assembly') -> '_6528.AssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_guide_dxf_model(self, design_entity: '_2191.GuideDxfModel') -> '_6606.GuideDxfModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_mass_disc(self, design_entity: '_2198.MassDisc') -> '_6633.MassDiscLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_measurement_component(self, design_entity: '_2199.MeasurementComponent') -> '_6634.MeasurementComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_mountable_component(self, design_entity: '_2200.MountableComponent') -> '_6637.MountableComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_oil_seal(self, design_entity: '_2202.OilSeal') -> '_6639.OilSealLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_part(self, design_entity: '_2204.Part') -> '_6641.PartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_planet_carrier(self, design_entity: '_2205.PlanetCarrier') -> '_6648.PlanetCarrierLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_point_load(self, design_entity: '_2207.PointLoad') -> '_6651.PointLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_power_load(self, design_entity: '_2208.PowerLoad') -> '_6652.PowerLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_root_assembly(self, design_entity: '_2210.RootAssembly') -> '_6661.RootAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_specialised_assembly(self, design_entity: '_2212.SpecialisedAssembly') -> '_6665.SpecialisedAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2213.UnbalancedMass') -> '_6694.UnbalancedMassLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_virtual_component(self, design_entity: '_2215.VirtualComponent') -> '_6695.VirtualComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_shaft(self, design_entity: '_2218.Shaft') -> '_6663.ShaftLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_gear(self, design_entity: '_2256.ConceptGear') -> '_6550.ConceptGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_set(self, design_entity: '_2257.ConceptGearSet') -> '_6552.ConceptGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_face_gear(self, design_entity: '_2263.FaceGear') -> '_6594.FaceGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_face_gear_set(self, design_entity: '_2264.FaceGearSet') -> '_6596.FaceGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2248.AGMAGleasonConicalGear') -> '_6523.AGMAGleasonConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2249.AGMAGleasonConicalGearSet') -> '_6525.AGMAGleasonConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2250.BevelDifferentialGear') -> '_6532.BevelDifferentialGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2251.BevelDifferentialGearSet') -> '_6534.BevelDifferentialGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2252.BevelDifferentialPlanetGear') -> '_6535.BevelDifferentialPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2253.BevelDifferentialSunGear') -> '_6536.BevelDifferentialSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear(self, design_entity: '_2254.BevelGear') -> '_6537.BevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2255.BevelGearSet') -> '_6539.BevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_conical_gear(self, design_entity: '_2258.ConicalGear') -> '_6553.ConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_set(self, design_entity: '_2259.ConicalGearSet') -> '_6557.ConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2260.CylindricalGear') -> '_6570.CylindricalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2261.CylindricalGearSet') -> '_6574.CylindricalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2262.CylindricalPlanetGear') -> '_6575.CylindricalPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_gear(self, design_entity: '_2265.Gear') -> '_6600.GearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_gear_set(self, design_entity: '_2267.GearSet') -> '_6605.GearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear(self, design_entity: '_2269.HypoidGear') -> '_6617.HypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2270.HypoidGearSet') -> '_6619.HypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2271.KlingelnbergCycloPalloidConicalGear') -> '_6624.KlingelnbergCycloPalloidConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2272.KlingelnbergCycloPalloidConicalGearSet') -> '_6626.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2273.KlingelnbergCycloPalloidHypoidGear') -> '_6627.KlingelnbergCycloPalloidHypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2274.KlingelnbergCycloPalloidHypoidGearSet') -> '_6629.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2275.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6630.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2276.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6632.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2277.PlanetaryGearSet') -> '_6646.PlanetaryGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2278.SpiralBevelGear') -> '_6667.SpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2279.SpiralBevelGearSet') -> '_6669.SpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2280.StraightBevelDiffGear') -> '_6673.StraightBevelDiffGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2281.StraightBevelDiffGearSet') -> '_6675.StraightBevelDiffGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2282.StraightBevelGear') -> '_6676.StraightBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2283.StraightBevelGearSet') -> '_6678.StraightBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2284.StraightBevelPlanetGear') -> '_6679.StraightBevelPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2285.StraightBevelSunGear') -> '_6680.StraightBevelSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_worm_gear(self, design_entity: '_2286.WormGear') -> '_6696.WormGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_set(self, design_entity: '_2287.WormGearSet') -> '_6698.WormGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2288.ZerolBevelGear') -> '_6699.ZerolBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2289.ZerolBevelGearSet') -> '_6701.ZerolBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_assembly(self, design_entity: '_2303.CycloidalAssembly') -> '_6566.CycloidalAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc(self, design_entity: '_2304.CycloidalDisc') -> '_6568.CycloidalDiscLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_ring_pins(self, design_entity: '_2305.RingPins') -> '_6656.RingPinsLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2323.PartToPartShearCoupling') -> '_6644.PartToPartShearCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2324.PartToPartShearCouplingHalf') -> '_6643.PartToPartShearCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_belt_drive(self, design_entity: '_2311.BeltDrive') -> '_6531.BeltDriveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_clutch(self, design_entity: '_2313.Clutch') -> '_6544.ClutchLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_clutch_half(self, design_entity: '_2314.ClutchHalf') -> '_6543.ClutchHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling(self, design_entity: '_2316.ConceptCoupling') -> '_6549.ConceptCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2317.ConceptCouplingHalf') -> '_6548.ConceptCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_coupling(self, design_entity: '_2318.Coupling') -> '_6562.CouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_coupling_half(self, design_entity: '_2319.CouplingHalf') -> '_6561.CouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cvt(self, design_entity: '_2321.CVT') -> '_6564.CVTLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cvt_pulley(self, design_entity: '_2322.CVTPulley') -> '_6565.CVTPulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_pulley(self, design_entity: '_2325.Pulley') -> '_6653.PulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2333.ShaftHubConnection') -> '_6662.ShaftHubConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring(self, design_entity: '_2331.RollingRing') -> '_6660.RollingRingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2332.RollingRingAssembly') -> '_6658.RollingRingAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spring_damper(self, design_entity: '_2335.SpringDamper') -> '_6672.SpringDamperLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_half(self, design_entity: '_2336.SpringDamperHalf') -> '_6671.SpringDamperHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_synchroniser(self, design_entity: '_2337.Synchroniser') -> '_6682.SynchroniserLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_half(self, design_entity: '_2339.SynchroniserHalf') -> '_6681.SynchroniserHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_part(self, design_entity: '_2340.SynchroniserPart') -> '_6683.SynchroniserPartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2341.SynchroniserSleeve') -> '_6684.SynchroniserSleeveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_torque_converter(self, design_entity: '_2342.TorqueConverter') -> '_6687.TorqueConverterLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2343.TorqueConverterPump') -> '_6688.TorqueConverterPumpLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2345.TorqueConverterTurbine') -> '_6689.TorqueConverterTurbineLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_2032.ShaftToMountableComponentConnection') -> '_6664.ShaftToMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_2010.CVTBeltConnection') -> '_6563.CVTBeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_belt_connection(self, design_entity: '_2005.BeltConnection') -> '_6530.BeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_coaxial_connection(self, design_entity: '_2006.CoaxialConnection') -> '_6545.CoaxialConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_connection(self, design_entity: '_2009.Connection') -> '_6558.ConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_2018.InterMountableComponentConnection') -> '_6623.InterMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_planetary_connection(self, design_entity: '_2024.PlanetaryConnection') -> '_6645.PlanetaryConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_2029.RollingRingConnection') -> '_6659.RollingRingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_2002.AbstractShaftToMountableComponentConnection') -> '_6519.AbstractShaftToMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_2038.BevelDifferentialGearMesh') -> '_6533.BevelDifferentialGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_2042.ConceptGearMesh') -> '_6551.ConceptGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_face_gear_mesh(self, design_entity: '_2048.FaceGearMesh') -> '_6595.FaceGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_2062.StraightBevelDiffGearMesh') -> '_6674.StraightBevelDiffGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_2040.BevelGearMesh') -> '_6538.BevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_2044.ConicalGearMesh') -> '_6555.ConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_2036.AGMAGleasonConicalGearMesh') -> '_6524.AGMAGleasonConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_2046.CylindricalGearMesh') -> '_6572.CylindricalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_2052.HypoidGearMesh') -> '_6618.HypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_2055.KlingelnbergCycloPalloidConicalGearMesh') -> '_6625.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_2056.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6628.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6631.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_2060.SpiralBevelGearMesh') -> '_6668.SpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_2064.StraightBevelGearMesh') -> '_6677.StraightBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_2066.WormGearMesh') -> '_6697.WormGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_2068.ZerolBevelGearMesh') -> '_6700.ZerolBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_gear_mesh(self, design_entity: '_2050.GearMesh') -> '_6602.GearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_2072.CycloidalDiscCentralBearingConnection') -> '_6567.CycloidalDiscCentralBearingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_2075.CycloidalDiscPlanetaryBearingConnection') -> '_6569.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_ring_pins_to_disc_connection(self, design_entity: '_2078.RingPinsToDiscConnection') -> '_6657.RingPinsToDiscConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_2085.PartToPartShearCouplingConnection') -> '_6642.PartToPartShearCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_clutch_connection(self, design_entity: '_2079.ClutchConnection') -> '_6542.ClutchConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_2081.ConceptCouplingConnection') -> '_6547.ConceptCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_coupling_connection(self, design_entity: '_2083.CouplingConnection') -> '_6560.CouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_connection(self, design_entity: '_2087.SpringDamperConnection') -> '_6670.SpringDamperConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
