﻿'''_5665.py

AssemblyHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6528, _6661
from mastapy.system_model.analyses_and_results.system_deflections import _2427, _2530
from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5735, _5666, _5668, _5671,
    _5678, _5677, _5681, _5687,
    _5690, _5700, _5702, _5704,
    _5708, _5726, _5727, _5728,
    _5746, _5753, _5756, _5757,
    _5758, _5760, _5764, _5768,
    _5769, _5770, _5779, _5772,
    _5774, _5778, _5786, _5789,
    _5792, _5795, _5799, _5803,
    _5807, _5811, _5814, _5657
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AssemblyHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyHarmonicAnalysis',)


class AssemblyHarmonicAnalysis(_5657.AbstractAssemblyHarmonicAnalysis):
    '''AssemblyHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2427.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2427.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def loaded_gear_sets(self) -> 'List[_5735.GearSetHarmonicAnalysis]':
        '''List[GearSetHarmonicAnalysis]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedGearSets, constructor.new(_5735.GearSetHarmonicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5666.BearingHarmonicAnalysis]':
        '''List[BearingHarmonicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5666.BearingHarmonicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5668.BeltDriveHarmonicAnalysis]':
        '''List[BeltDriveHarmonicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5668.BeltDriveHarmonicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5671.BevelDifferentialGearSetHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetHarmonicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5671.BevelDifferentialGearSetHarmonicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5678.BoltHarmonicAnalysis]':
        '''List[BoltHarmonicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5678.BoltHarmonicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5677.BoltedJointHarmonicAnalysis]':
        '''List[BoltedJointHarmonicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5677.BoltedJointHarmonicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5681.ClutchHarmonicAnalysis]':
        '''List[ClutchHarmonicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5681.ClutchHarmonicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5687.ConceptCouplingHarmonicAnalysis]':
        '''List[ConceptCouplingHarmonicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5687.ConceptCouplingHarmonicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5690.ConceptGearSetHarmonicAnalysis]':
        '''List[ConceptGearSetHarmonicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5690.ConceptGearSetHarmonicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5700.CVTHarmonicAnalysis]':
        '''List[CVTHarmonicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5700.CVTHarmonicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5702.CycloidalAssemblyHarmonicAnalysis]':
        '''List[CycloidalAssemblyHarmonicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5702.CycloidalAssemblyHarmonicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5704.CycloidalDiscHarmonicAnalysis]':
        '''List[CycloidalDiscHarmonicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5704.CycloidalDiscHarmonicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5708.CylindricalGearSetHarmonicAnalysis]':
        '''List[CylindricalGearSetHarmonicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5708.CylindricalGearSetHarmonicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5726.FaceGearSetHarmonicAnalysis]':
        '''List[FaceGearSetHarmonicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5726.FaceGearSetHarmonicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5727.FEPartHarmonicAnalysis]':
        '''List[FEPartHarmonicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5727.FEPartHarmonicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5728.FlexiblePinAssemblyHarmonicAnalysis]':
        '''List[FlexiblePinAssemblyHarmonicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5728.FlexiblePinAssemblyHarmonicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5746.HypoidGearSetHarmonicAnalysis]':
        '''List[HypoidGearSetHarmonicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5746.HypoidGearSetHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5753.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5753.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5756.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5756.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5757.MassDiscHarmonicAnalysis]':
        '''List[MassDiscHarmonicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5757.MassDiscHarmonicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5758.MeasurementComponentHarmonicAnalysis]':
        '''List[MeasurementComponentHarmonicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5758.MeasurementComponentHarmonicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5760.OilSealHarmonicAnalysis]':
        '''List[OilSealHarmonicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5760.OilSealHarmonicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5764.PartToPartShearCouplingHarmonicAnalysis]':
        '''List[PartToPartShearCouplingHarmonicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5764.PartToPartShearCouplingHarmonicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5768.PlanetCarrierHarmonicAnalysis]':
        '''List[PlanetCarrierHarmonicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5768.PlanetCarrierHarmonicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5769.PointLoadHarmonicAnalysis]':
        '''List[PointLoadHarmonicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5769.PointLoadHarmonicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5770.PowerLoadHarmonicAnalysis]':
        '''List[PowerLoadHarmonicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5770.PowerLoadHarmonicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5779.ShaftHubConnectionHarmonicAnalysis]':
        '''List[ShaftHubConnectionHarmonicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5779.ShaftHubConnectionHarmonicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5772.RingPinsHarmonicAnalysis]':
        '''List[RingPinsHarmonicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5772.RingPinsHarmonicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5774.RollingRingAssemblyHarmonicAnalysis]':
        '''List[RollingRingAssemblyHarmonicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5774.RollingRingAssemblyHarmonicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5778.ShaftHarmonicAnalysis]':
        '''List[ShaftHarmonicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5778.ShaftHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5786.SpiralBevelGearSetHarmonicAnalysis]':
        '''List[SpiralBevelGearSetHarmonicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5786.SpiralBevelGearSetHarmonicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5789.SpringDamperHarmonicAnalysis]':
        '''List[SpringDamperHarmonicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5789.SpringDamperHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5792.StraightBevelDiffGearSetHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5792.StraightBevelDiffGearSetHarmonicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5795.StraightBevelGearSetHarmonicAnalysis]':
        '''List[StraightBevelGearSetHarmonicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5795.StraightBevelGearSetHarmonicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5799.SynchroniserHarmonicAnalysis]':
        '''List[SynchroniserHarmonicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5799.SynchroniserHarmonicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5803.TorqueConverterHarmonicAnalysis]':
        '''List[TorqueConverterHarmonicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5803.TorqueConverterHarmonicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5807.UnbalancedMassHarmonicAnalysis]':
        '''List[UnbalancedMassHarmonicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5807.UnbalancedMassHarmonicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5811.WormGearSetHarmonicAnalysis]':
        '''List[WormGearSetHarmonicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5811.WormGearSetHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5814.ZerolBevelGearSetHarmonicAnalysis]':
        '''List[ZerolBevelGearSetHarmonicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5814.ZerolBevelGearSetHarmonicAnalysis))
        return value
