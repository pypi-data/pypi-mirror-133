'''_4029.py

AssemblyParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2171, _2210
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6528, _6661
from mastapy.system_model.analyses_and_results.parametric_study_tools import (
    _4076, _4030, _4032, _4035,
    _4042, _4041, _4045, _4050,
    _4053, _4063, _4065, _4067,
    _4071, _4084, _4085, _4086,
    _4093, _4100, _4103, _4104,
    _4105, _4108, _4122, _4125,
    _4126, _4127, _4135, _4129,
    _4131, _4136, _4141, _4144,
    _4147, _4150, _4154, _4158,
    _4161, _4165, _4168, _4022
)
from mastapy.system_model.analyses_and_results.system_deflections import _2427
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'AssemblyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyParametricStudyTool',)


class AssemblyParametricStudyTool(_4022.AbstractAssemblyParametricStudyTool):
    '''AssemblyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyParametricStudyTool.TYPE'):
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
    def all_duty_cycle_results(self) -> 'List[_4076.DutyCycleResultsForAllComponents]':
        '''List[DutyCycleResultsForAllComponents]: 'AllDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllDutyCycleResults, constructor.new(_4076.DutyCycleResultsForAllComponents))
        return value

    @property
    def bearings(self) -> 'List[_4030.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4030.BearingParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_4032.BeltDriveParametricStudyTool]':
        '''List[BeltDriveParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4032.BeltDriveParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4035.BevelDifferentialGearSetParametricStudyTool]':
        '''List[BevelDifferentialGearSetParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4035.BevelDifferentialGearSetParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_4042.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4042.BoltParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_4041.BoltedJointParametricStudyTool]':
        '''List[BoltedJointParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4041.BoltedJointParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_4045.ClutchParametricStudyTool]':
        '''List[ClutchParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4045.ClutchParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_4050.ConceptCouplingParametricStudyTool]':
        '''List[ConceptCouplingParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4050.ConceptCouplingParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4053.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4053.ConceptGearSetParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_4063.CVTParametricStudyTool]':
        '''List[CVTParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4063.CVTParametricStudyTool))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4065.CycloidalAssemblyParametricStudyTool]':
        '''List[CycloidalAssemblyParametricStudyTool]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4065.CycloidalAssemblyParametricStudyTool))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4067.CycloidalDiscParametricStudyTool]':
        '''List[CycloidalDiscParametricStudyTool]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4067.CycloidalDiscParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4071.CylindricalGearSetParametricStudyTool]':
        '''List[CylindricalGearSetParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4071.CylindricalGearSetParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4084.FaceGearSetParametricStudyTool]':
        '''List[FaceGearSetParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4084.FaceGearSetParametricStudyTool))
        return value

    @property
    def fe_parts(self) -> 'List[_4085.FEPartParametricStudyTool]':
        '''List[FEPartParametricStudyTool]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4085.FEPartParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4086.FlexiblePinAssemblyParametricStudyTool]':
        '''List[FlexiblePinAssemblyParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4086.FlexiblePinAssemblyParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4093.HypoidGearSetParametricStudyTool]':
        '''List[HypoidGearSetParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4093.HypoidGearSetParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4100.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4100.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4103.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4103.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_4104.MassDiscParametricStudyTool]':
        '''List[MassDiscParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4104.MassDiscParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_4105.MeasurementComponentParametricStudyTool]':
        '''List[MeasurementComponentParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4105.MeasurementComponentParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_4108.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4108.OilSealParametricStudyTool))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4122.PartToPartShearCouplingParametricStudyTool]':
        '''List[PartToPartShearCouplingParametricStudyTool]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4122.PartToPartShearCouplingParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_4125.PlanetCarrierParametricStudyTool]':
        '''List[PlanetCarrierParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4125.PlanetCarrierParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_4126.PointLoadParametricStudyTool]':
        '''List[PointLoadParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4126.PointLoadParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_4127.PowerLoadParametricStudyTool]':
        '''List[PowerLoadParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4127.PowerLoadParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4135.ShaftHubConnectionParametricStudyTool]':
        '''List[ShaftHubConnectionParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4135.ShaftHubConnectionParametricStudyTool))
        return value

    @property
    def ring_pins(self) -> 'List[_4129.RingPinsParametricStudyTool]':
        '''List[RingPinsParametricStudyTool]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4129.RingPinsParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4131.RollingRingAssemblyParametricStudyTool]':
        '''List[RollingRingAssemblyParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4131.RollingRingAssemblyParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_4136.ShaftParametricStudyTool]':
        '''List[ShaftParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4136.ShaftParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4141.SpiralBevelGearSetParametricStudyTool]':
        '''List[SpiralBevelGearSetParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4141.SpiralBevelGearSetParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_4144.SpringDamperParametricStudyTool]':
        '''List[SpringDamperParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4144.SpringDamperParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4147.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4147.StraightBevelDiffGearSetParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4150.StraightBevelGearSetParametricStudyTool]':
        '''List[StraightBevelGearSetParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4150.StraightBevelGearSetParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_4154.SynchroniserParametricStudyTool]':
        '''List[SynchroniserParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4154.SynchroniserParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_4158.TorqueConverterParametricStudyTool]':
        '''List[TorqueConverterParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4158.TorqueConverterParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4161.UnbalancedMassParametricStudyTool]':
        '''List[UnbalancedMassParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4161.UnbalancedMassParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4165.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4165.WormGearSetParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4168.ZerolBevelGearSetParametricStudyTool]':
        '''List[ZerolBevelGearSetParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4168.ZerolBevelGearSetParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2427.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2427.AssemblySystemDeflection))
        return value
