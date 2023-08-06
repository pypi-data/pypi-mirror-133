'''_3767.py

AssemblyPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6528, _6661
from mastapy.gears.analysis import _1166
from mastapy.system_model.analyses_and_results.power_flows import (
    _3768, _3770, _3773, _3780,
    _3779, _3783, _3788, _3791,
    _3801, _3803, _3806, _3810,
    _3816, _3817, _3818, _3825,
    _3832, _3835, _3836, _3837,
    _3839, _3843, _3846, _3847,
    _3850, _3858, _3852, _3854,
    _3859, _3864, _3867, _3870,
    _3873, _3878, _3882, _3885,
    _3889, _3892, _3821, _3760
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'AssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyPowerFlow',)


class AssemblyPowerFlow(_3760.AbstractAssemblyPowerFlow):
    '''AssemblyPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6528.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6528.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def rating_for_all_gear_sets(self) -> '_1166.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1166.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets is not None else None

    @property
    def bearings(self) -> 'List[_3768.BearingPowerFlow]':
        '''List[BearingPowerFlow]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3768.BearingPowerFlow))
        return value

    @property
    def belt_drives(self) -> 'List[_3770.BeltDrivePowerFlow]':
        '''List[BeltDrivePowerFlow]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3770.BeltDrivePowerFlow))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3773.BevelDifferentialGearSetPowerFlow]':
        '''List[BevelDifferentialGearSetPowerFlow]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3773.BevelDifferentialGearSetPowerFlow))
        return value

    @property
    def bolts(self) -> 'List[_3780.BoltPowerFlow]':
        '''List[BoltPowerFlow]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3780.BoltPowerFlow))
        return value

    @property
    def bolted_joints(self) -> 'List[_3779.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3779.BoltedJointPowerFlow))
        return value

    @property
    def clutches(self) -> 'List[_3783.ClutchPowerFlow]':
        '''List[ClutchPowerFlow]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3783.ClutchPowerFlow))
        return value

    @property
    def concept_couplings(self) -> 'List[_3788.ConceptCouplingPowerFlow]':
        '''List[ConceptCouplingPowerFlow]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3788.ConceptCouplingPowerFlow))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3791.ConceptGearSetPowerFlow]':
        '''List[ConceptGearSetPowerFlow]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3791.ConceptGearSetPowerFlow))
        return value

    @property
    def cv_ts(self) -> 'List[_3801.CVTPowerFlow]':
        '''List[CVTPowerFlow]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3801.CVTPowerFlow))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3803.CycloidalAssemblyPowerFlow]':
        '''List[CycloidalAssemblyPowerFlow]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3803.CycloidalAssemblyPowerFlow))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3806.CycloidalDiscPowerFlow]':
        '''List[CycloidalDiscPowerFlow]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3806.CycloidalDiscPowerFlow))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3810.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3810.CylindricalGearSetPowerFlow))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3816.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3816.FaceGearSetPowerFlow))
        return value

    @property
    def fe_parts(self) -> 'List[_3817.FEPartPowerFlow]':
        '''List[FEPartPowerFlow]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3817.FEPartPowerFlow))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3818.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3818.FlexiblePinAssemblyPowerFlow))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3825.HypoidGearSetPowerFlow]':
        '''List[HypoidGearSetPowerFlow]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3825.HypoidGearSetPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3832.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3832.KlingelnbergCycloPalloidHypoidGearSetPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3835.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3835.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow))
        return value

    @property
    def mass_discs(self) -> 'List[_3836.MassDiscPowerFlow]':
        '''List[MassDiscPowerFlow]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3836.MassDiscPowerFlow))
        return value

    @property
    def measurement_components(self) -> 'List[_3837.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3837.MeasurementComponentPowerFlow))
        return value

    @property
    def oil_seals(self) -> 'List[_3839.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3839.OilSealPowerFlow))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3843.PartToPartShearCouplingPowerFlow]':
        '''List[PartToPartShearCouplingPowerFlow]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3843.PartToPartShearCouplingPowerFlow))
        return value

    @property
    def planet_carriers(self) -> 'List[_3846.PlanetCarrierPowerFlow]':
        '''List[PlanetCarrierPowerFlow]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3846.PlanetCarrierPowerFlow))
        return value

    @property
    def point_loads(self) -> 'List[_3847.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3847.PointLoadPowerFlow))
        return value

    @property
    def power_loads(self) -> 'List[_3850.PowerLoadPowerFlow]':
        '''List[PowerLoadPowerFlow]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3850.PowerLoadPowerFlow))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3858.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3858.ShaftHubConnectionPowerFlow))
        return value

    @property
    def ring_pins(self) -> 'List[_3852.RingPinsPowerFlow]':
        '''List[RingPinsPowerFlow]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3852.RingPinsPowerFlow))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3854.RollingRingAssemblyPowerFlow]':
        '''List[RollingRingAssemblyPowerFlow]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3854.RollingRingAssemblyPowerFlow))
        return value

    @property
    def shafts(self) -> 'List[_3859.ShaftPowerFlow]':
        '''List[ShaftPowerFlow]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3859.ShaftPowerFlow))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3864.SpiralBevelGearSetPowerFlow]':
        '''List[SpiralBevelGearSetPowerFlow]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3864.SpiralBevelGearSetPowerFlow))
        return value

    @property
    def spring_dampers(self) -> 'List[_3867.SpringDamperPowerFlow]':
        '''List[SpringDamperPowerFlow]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3867.SpringDamperPowerFlow))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3870.StraightBevelDiffGearSetPowerFlow]':
        '''List[StraightBevelDiffGearSetPowerFlow]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3870.StraightBevelDiffGearSetPowerFlow))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3873.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3873.StraightBevelGearSetPowerFlow))
        return value

    @property
    def synchronisers(self) -> 'List[_3878.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3878.SynchroniserPowerFlow))
        return value

    @property
    def torque_converters(self) -> 'List[_3882.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3882.TorqueConverterPowerFlow))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3885.UnbalancedMassPowerFlow]':
        '''List[UnbalancedMassPowerFlow]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3885.UnbalancedMassPowerFlow))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3889.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3889.WormGearSetPowerFlow))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3892.ZerolBevelGearSetPowerFlow]':
        '''List[ZerolBevelGearSetPowerFlow]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3892.ZerolBevelGearSetPowerFlow))
        return value

    @property
    def loaded_gear_sets(self) -> 'List[_3821.GearSetPowerFlow]':
        '''List[GearSetPowerFlow]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedGearSets, constructor.new(_3821.GearSetPowerFlow))
        return value
