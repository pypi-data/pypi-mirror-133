'''_3900.py

AssemblyCompoundPowerFlow
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal.cast_exception import CastException
from mastapy.gears.analysis import _1166
from mastapy.system_model.analyses_and_results.power_flows import _3767
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3901, _3903, _3906, _3912,
    _3913, _3914, _3919, _3924,
    _3934, _3936, _3938, _3942,
    _3948, _3949, _3950, _3957,
    _3964, _3967, _3968, _3969,
    _3971, _3973, _3978, _3979,
    _3980, _3989, _3982, _3984,
    _3988, _3994, _3995, _4000,
    _4003, _4006, _4010, _4014,
    _4018, _4021, _3893
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundPowerFlow',)


class AssemblyCompoundPowerFlow(_3893.AbstractAssemblyCompoundPowerFlow):
    '''AssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def input_power_load_ratio_warning(self) -> 'str':
        '''str: 'InputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InputPowerLoadRatioWarning

    @property
    def output_power_load_ratio_warning(self) -> 'str':
        '''str: 'OutputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OutputPowerLoadRatioWarning

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
    def rating_for_all_gear_sets(self) -> '_1166.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1166.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3767.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3767.AssemblyPowerFlow))
        return value

    @property
    def bearings(self) -> 'List[_3901.BearingCompoundPowerFlow]':
        '''List[BearingCompoundPowerFlow]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3901.BearingCompoundPowerFlow))
        return value

    @property
    def belt_drives(self) -> 'List[_3903.BeltDriveCompoundPowerFlow]':
        '''List[BeltDriveCompoundPowerFlow]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3903.BeltDriveCompoundPowerFlow))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3906.BevelDifferentialGearSetCompoundPowerFlow]':
        '''List[BevelDifferentialGearSetCompoundPowerFlow]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3906.BevelDifferentialGearSetCompoundPowerFlow))
        return value

    @property
    def bolts(self) -> 'List[_3912.BoltCompoundPowerFlow]':
        '''List[BoltCompoundPowerFlow]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3912.BoltCompoundPowerFlow))
        return value

    @property
    def bolted_joints(self) -> 'List[_3913.BoltedJointCompoundPowerFlow]':
        '''List[BoltedJointCompoundPowerFlow]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3913.BoltedJointCompoundPowerFlow))
        return value

    @property
    def clutches(self) -> 'List[_3914.ClutchCompoundPowerFlow]':
        '''List[ClutchCompoundPowerFlow]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3914.ClutchCompoundPowerFlow))
        return value

    @property
    def concept_couplings(self) -> 'List[_3919.ConceptCouplingCompoundPowerFlow]':
        '''List[ConceptCouplingCompoundPowerFlow]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3919.ConceptCouplingCompoundPowerFlow))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3924.ConceptGearSetCompoundPowerFlow]':
        '''List[ConceptGearSetCompoundPowerFlow]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3924.ConceptGearSetCompoundPowerFlow))
        return value

    @property
    def cv_ts(self) -> 'List[_3934.CVTCompoundPowerFlow]':
        '''List[CVTCompoundPowerFlow]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3934.CVTCompoundPowerFlow))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3936.CycloidalAssemblyCompoundPowerFlow]':
        '''List[CycloidalAssemblyCompoundPowerFlow]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3936.CycloidalAssemblyCompoundPowerFlow))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3938.CycloidalDiscCompoundPowerFlow]':
        '''List[CycloidalDiscCompoundPowerFlow]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3938.CycloidalDiscCompoundPowerFlow))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3942.CylindricalGearSetCompoundPowerFlow]':
        '''List[CylindricalGearSetCompoundPowerFlow]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3942.CylindricalGearSetCompoundPowerFlow))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3948.FaceGearSetCompoundPowerFlow]':
        '''List[FaceGearSetCompoundPowerFlow]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3948.FaceGearSetCompoundPowerFlow))
        return value

    @property
    def fe_parts(self) -> 'List[_3949.FEPartCompoundPowerFlow]':
        '''List[FEPartCompoundPowerFlow]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3949.FEPartCompoundPowerFlow))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3950.FlexiblePinAssemblyCompoundPowerFlow]':
        '''List[FlexiblePinAssemblyCompoundPowerFlow]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3950.FlexiblePinAssemblyCompoundPowerFlow))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3957.HypoidGearSetCompoundPowerFlow]':
        '''List[HypoidGearSetCompoundPowerFlow]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3957.HypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3964.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3964.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3967.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3967.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def mass_discs(self) -> 'List[_3968.MassDiscCompoundPowerFlow]':
        '''List[MassDiscCompoundPowerFlow]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3968.MassDiscCompoundPowerFlow))
        return value

    @property
    def measurement_components(self) -> 'List[_3969.MeasurementComponentCompoundPowerFlow]':
        '''List[MeasurementComponentCompoundPowerFlow]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3969.MeasurementComponentCompoundPowerFlow))
        return value

    @property
    def oil_seals(self) -> 'List[_3971.OilSealCompoundPowerFlow]':
        '''List[OilSealCompoundPowerFlow]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3971.OilSealCompoundPowerFlow))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3973.PartToPartShearCouplingCompoundPowerFlow]':
        '''List[PartToPartShearCouplingCompoundPowerFlow]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3973.PartToPartShearCouplingCompoundPowerFlow))
        return value

    @property
    def planet_carriers(self) -> 'List[_3978.PlanetCarrierCompoundPowerFlow]':
        '''List[PlanetCarrierCompoundPowerFlow]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3978.PlanetCarrierCompoundPowerFlow))
        return value

    @property
    def point_loads(self) -> 'List[_3979.PointLoadCompoundPowerFlow]':
        '''List[PointLoadCompoundPowerFlow]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3979.PointLoadCompoundPowerFlow))
        return value

    @property
    def power_loads(self) -> 'List[_3980.PowerLoadCompoundPowerFlow]':
        '''List[PowerLoadCompoundPowerFlow]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3980.PowerLoadCompoundPowerFlow))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3989.ShaftHubConnectionCompoundPowerFlow]':
        '''List[ShaftHubConnectionCompoundPowerFlow]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3989.ShaftHubConnectionCompoundPowerFlow))
        return value

    @property
    def ring_pins(self) -> 'List[_3982.RingPinsCompoundPowerFlow]':
        '''List[RingPinsCompoundPowerFlow]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3982.RingPinsCompoundPowerFlow))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3984.RollingRingAssemblyCompoundPowerFlow]':
        '''List[RollingRingAssemblyCompoundPowerFlow]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3984.RollingRingAssemblyCompoundPowerFlow))
        return value

    @property
    def shafts(self) -> 'List[_3988.ShaftCompoundPowerFlow]':
        '''List[ShaftCompoundPowerFlow]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3988.ShaftCompoundPowerFlow))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3994.SpiralBevelGearSetCompoundPowerFlow]':
        '''List[SpiralBevelGearSetCompoundPowerFlow]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3994.SpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def spring_dampers(self) -> 'List[_3995.SpringDamperCompoundPowerFlow]':
        '''List[SpringDamperCompoundPowerFlow]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3995.SpringDamperCompoundPowerFlow))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4000.StraightBevelDiffGearSetCompoundPowerFlow]':
        '''List[StraightBevelDiffGearSetCompoundPowerFlow]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4000.StraightBevelDiffGearSetCompoundPowerFlow))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4003.StraightBevelGearSetCompoundPowerFlow]':
        '''List[StraightBevelGearSetCompoundPowerFlow]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4003.StraightBevelGearSetCompoundPowerFlow))
        return value

    @property
    def synchronisers(self) -> 'List[_4006.SynchroniserCompoundPowerFlow]':
        '''List[SynchroniserCompoundPowerFlow]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4006.SynchroniserCompoundPowerFlow))
        return value

    @property
    def torque_converters(self) -> 'List[_4010.TorqueConverterCompoundPowerFlow]':
        '''List[TorqueConverterCompoundPowerFlow]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4010.TorqueConverterCompoundPowerFlow))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4014.UnbalancedMassCompoundPowerFlow]':
        '''List[UnbalancedMassCompoundPowerFlow]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4014.UnbalancedMassCompoundPowerFlow))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4018.WormGearSetCompoundPowerFlow]':
        '''List[WormGearSetCompoundPowerFlow]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4018.WormGearSetCompoundPowerFlow))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4021.ZerolBevelGearSetCompoundPowerFlow]':
        '''List[ZerolBevelGearSetCompoundPowerFlow]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4021.ZerolBevelGearSetCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3767.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3767.AssemblyPowerFlow))
        return value
