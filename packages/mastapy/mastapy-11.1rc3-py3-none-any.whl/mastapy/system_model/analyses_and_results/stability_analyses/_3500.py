'''_3500.py

AssemblyStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6528, _6661
from mastapy.system_model.analyses_and_results.stability_analyses import (
    _3501, _3503, _3505, _3513,
    _3512, _3516, _3521, _3523,
    _3536, _3537, _3540, _3542,
    _3548, _3550, _3551, _3557,
    _3564, _3567, _3569, _3570,
    _3572, _3576, _3579, _3580,
    _3581, _3589, _3583, _3585,
    _3590, _3594, _3598, _3602,
    _3605, _3612, _3615, _3617,
    _3620, _3623, _3493
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'AssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyStabilityAnalysis',)


class AssemblyStabilityAnalysis(_3493.AbstractAssemblyStabilityAnalysis):
    '''AssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyStabilityAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_3501.BearingStabilityAnalysis]':
        '''List[BearingStabilityAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3501.BearingStabilityAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3503.BeltDriveStabilityAnalysis]':
        '''List[BeltDriveStabilityAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3503.BeltDriveStabilityAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3505.BevelDifferentialGearSetStabilityAnalysis]':
        '''List[BevelDifferentialGearSetStabilityAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3505.BevelDifferentialGearSetStabilityAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3513.BoltStabilityAnalysis]':
        '''List[BoltStabilityAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3513.BoltStabilityAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3512.BoltedJointStabilityAnalysis]':
        '''List[BoltedJointStabilityAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3512.BoltedJointStabilityAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3516.ClutchStabilityAnalysis]':
        '''List[ClutchStabilityAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3516.ClutchStabilityAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3521.ConceptCouplingStabilityAnalysis]':
        '''List[ConceptCouplingStabilityAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3521.ConceptCouplingStabilityAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3523.ConceptGearSetStabilityAnalysis]':
        '''List[ConceptGearSetStabilityAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3523.ConceptGearSetStabilityAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3536.CVTStabilityAnalysis]':
        '''List[CVTStabilityAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3536.CVTStabilityAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3537.CycloidalAssemblyStabilityAnalysis]':
        '''List[CycloidalAssemblyStabilityAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3537.CycloidalAssemblyStabilityAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3540.CycloidalDiscStabilityAnalysis]':
        '''List[CycloidalDiscStabilityAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3540.CycloidalDiscStabilityAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3542.CylindricalGearSetStabilityAnalysis]':
        '''List[CylindricalGearSetStabilityAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3542.CylindricalGearSetStabilityAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3548.FaceGearSetStabilityAnalysis]':
        '''List[FaceGearSetStabilityAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3548.FaceGearSetStabilityAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_3550.FEPartStabilityAnalysis]':
        '''List[FEPartStabilityAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3550.FEPartStabilityAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3551.FlexiblePinAssemblyStabilityAnalysis]':
        '''List[FlexiblePinAssemblyStabilityAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3551.FlexiblePinAssemblyStabilityAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3557.HypoidGearSetStabilityAnalysis]':
        '''List[HypoidGearSetStabilityAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3557.HypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3564.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3564.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3567.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3567.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3569.MassDiscStabilityAnalysis]':
        '''List[MassDiscStabilityAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3569.MassDiscStabilityAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3570.MeasurementComponentStabilityAnalysis]':
        '''List[MeasurementComponentStabilityAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3570.MeasurementComponentStabilityAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3572.OilSealStabilityAnalysis]':
        '''List[OilSealStabilityAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3572.OilSealStabilityAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3576.PartToPartShearCouplingStabilityAnalysis]':
        '''List[PartToPartShearCouplingStabilityAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3576.PartToPartShearCouplingStabilityAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3579.PlanetCarrierStabilityAnalysis]':
        '''List[PlanetCarrierStabilityAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3579.PlanetCarrierStabilityAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3580.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3580.PointLoadStabilityAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3581.PowerLoadStabilityAnalysis]':
        '''List[PowerLoadStabilityAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3581.PowerLoadStabilityAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3589.ShaftHubConnectionStabilityAnalysis]':
        '''List[ShaftHubConnectionStabilityAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3589.ShaftHubConnectionStabilityAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_3583.RingPinsStabilityAnalysis]':
        '''List[RingPinsStabilityAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3583.RingPinsStabilityAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3585.RollingRingAssemblyStabilityAnalysis]':
        '''List[RollingRingAssemblyStabilityAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3585.RollingRingAssemblyStabilityAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3590.ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3590.ShaftStabilityAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3594.SpiralBevelGearSetStabilityAnalysis]':
        '''List[SpiralBevelGearSetStabilityAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3594.SpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3598.SpringDamperStabilityAnalysis]':
        '''List[SpringDamperStabilityAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3598.SpringDamperStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3602.StraightBevelDiffGearSetStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetStabilityAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3602.StraightBevelDiffGearSetStabilityAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3605.StraightBevelGearSetStabilityAnalysis]':
        '''List[StraightBevelGearSetStabilityAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3605.StraightBevelGearSetStabilityAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3612.SynchroniserStabilityAnalysis]':
        '''List[SynchroniserStabilityAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3612.SynchroniserStabilityAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3615.TorqueConverterStabilityAnalysis]':
        '''List[TorqueConverterStabilityAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3615.TorqueConverterStabilityAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3617.UnbalancedMassStabilityAnalysis]':
        '''List[UnbalancedMassStabilityAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3617.UnbalancedMassStabilityAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3620.WormGearSetStabilityAnalysis]':
        '''List[WormGearSetStabilityAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3620.WormGearSetStabilityAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3623.ZerolBevelGearSetStabilityAnalysis]':
        '''List[ZerolBevelGearSetStabilityAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3623.ZerolBevelGearSetStabilityAnalysis))
        return value
