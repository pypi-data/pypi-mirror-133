'''_2850.py

AssemblyCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2720
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _2851, _2853, _2856, _2862,
    _2863, _2864, _2869, _2874,
    _2884, _2886, _2888, _2892,
    _2898, _2899, _2900, _2907,
    _2914, _2917, _2918, _2919,
    _2921, _2923, _2928, _2929,
    _2930, _2939, _2932, _2934,
    _2938, _2944, _2945, _2950,
    _2953, _2956, _2960, _2964,
    _2968, _2971, _2843
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'AssemblyCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponseOnAShaft',)


class AssemblyCompoundSteadyStateSynchronousResponseOnAShaft(_2843.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft):
    '''AssemblyCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2171.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2171.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2720.AssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[AssemblySteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2720.AssemblySteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bearings(self) -> 'List[_2851.BearingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BearingCompoundSteadyStateSynchronousResponseOnAShaft]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2851.BearingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def belt_drives(self) -> 'List[_2853.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2853.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2856.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2856.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolts(self) -> 'List[_2862.BoltCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltCompoundSteadyStateSynchronousResponseOnAShaft]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2862.BoltCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolted_joints(self) -> 'List[_2863.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2863.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def clutches(self) -> 'List[_2864.ClutchCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ClutchCompoundSteadyStateSynchronousResponseOnAShaft]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2864.ClutchCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_couplings(self) -> 'List[_2869.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2869.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2874.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2874.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cv_ts(self) -> 'List[_2884.CVTCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CVTCompoundSteadyStateSynchronousResponseOnAShaft]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2884.CVTCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_2886.CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_2886.CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_2888.CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_2888.CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2892.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2892.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2898.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2898.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def fe_parts(self) -> 'List[_2899.FEPartCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[FEPartCompoundSteadyStateSynchronousResponseOnAShaft]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_2899.FEPartCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2900.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2900.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2907.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2907.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2914.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2914.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2917.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2917.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def mass_discs(self) -> 'List[_2918.MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2918.MassDiscCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def measurement_components(self) -> 'List[_2919.MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2919.MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def oil_seals(self) -> 'List[_2921.OilSealCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[OilSealCompoundSteadyStateSynchronousResponseOnAShaft]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2921.OilSealCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2923.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2923.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planet_carriers(self) -> 'List[_2928.PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2928.PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def point_loads(self) -> 'List[_2929.PointLoadCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponseOnAShaft]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2929.PointLoadCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def power_loads(self) -> 'List[_2930.PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2930.PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2939.ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2939.ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def ring_pins(self) -> 'List[_2932.RingPinsCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponseOnAShaft]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_2932.RingPinsCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2934.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2934.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shafts(self) -> 'List[_2938.ShaftCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftCompoundSteadyStateSynchronousResponseOnAShaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2938.ShaftCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2944.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2944.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spring_dampers(self) -> 'List[_2945.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2945.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2950.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2950.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2953.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2953.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def synchronisers(self) -> 'List[_2956.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2956.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def torque_converters(self) -> 'List[_2960.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2960.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2964.UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2964.UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2968.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2968.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2971.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2971.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2720.AssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[AssemblySteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2720.AssemblySteadyStateSynchronousResponseOnAShaft))
        return value
