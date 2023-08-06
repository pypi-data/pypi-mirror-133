﻿'''_901.py

GearMeshDesign
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs import _899, _900
from mastapy.gears.gear_designs.zerol_bevel import _904
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _908, _909, _912
from mastapy.gears.gear_designs.straight_bevel_diff import _913
from mastapy.gears.gear_designs.straight_bevel import _917
from mastapy.gears.gear_designs.spiral_bevel import _921
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _925
from mastapy.gears.gear_designs.klingelnberg_hypoid import _929
from mastapy.gears.gear_designs.klingelnberg_conical import _933
from mastapy.gears.gear_designs.hypoid import _937
from mastapy.gears.gear_designs.face import _941, _946, _949
from mastapy.gears.gear_designs.cylindrical import _964, _991
from mastapy.gears.gear_designs.conical import _1096
from mastapy.gears.gear_designs.concept import _1118
from mastapy.gears.gear_designs.bevel import _1122
from mastapy.gears.gear_designs.agma_gleason_conical import _1135
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'GearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshDesign',)


class GearMeshDesign(_900.GearDesignComponent):
    '''GearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def speed_ratio_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioAToB

    @property
    def torque_ratio_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioAToB

    @property
    def highest_common_factor_of_teeth_numbers(self) -> 'int':
        '''int: 'HighestCommonFactorOfTeethNumbers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HighestCommonFactorOfTeethNumbers

    @property
    def has_hunting_ratio(self) -> 'bool':
        '''bool: 'HasHuntingRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasHuntingRatio

    @property
    def hunting_tooth_factor(self) -> 'float':
        '''float: 'HuntingToothFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HuntingToothFactor

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def gear_a(self) -> '_899.GearDesign':
        '''GearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _899.GearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_zerol_bevel_gear_design(self) -> '_904.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.ZerolBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_design(self) -> '_908.WormDesign':
        '''WormDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.WormDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_gear_design(self) -> '_909.WormGearDesign':
        '''WormGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _909.WormGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_wheel_design(self) -> '_912.WormWheelDesign':
        '''WormWheelDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.WormWheelDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_straight_bevel_diff_gear_design(self) -> '_913.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_straight_bevel_gear_design(self) -> '_917.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.StraightBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_spiral_bevel_gear_design(self) -> '_921.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.SpiralBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_925.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_929.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_conical_gear_design(self) -> '_933.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_hypoid_gear_design(self) -> '_937.HypoidGearDesign':
        '''HypoidGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.HypoidGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_design(self) -> '_941.FaceGearDesign':
        '''FaceGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.FaceGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_pinion_design(self) -> '_946.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _946.FaceGearPinionDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_wheel_design(self) -> '_949.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _949.FaceGearWheelDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_design(self) -> '_964.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _964.CylindricalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_planet_gear_design(self) -> '_991.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _991.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_design(self) -> '_1096.ConicalGearDesign':
        '''ConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1096.ConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_concept_gear_design(self) -> '_1118.ConceptGearDesign':
        '''ConceptGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1118.ConceptGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_bevel_gear_design(self) -> '_1122.BevelGearDesign':
        '''BevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1122.BevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_agma_gleason_conical_gear_design(self) -> '_1135.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1135.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_b(self) -> '_899.GearDesign':
        '''GearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _899.GearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_zerol_bevel_gear_design(self) -> '_904.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.ZerolBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_design(self) -> '_908.WormDesign':
        '''WormDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.WormDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_gear_design(self) -> '_909.WormGearDesign':
        '''WormGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _909.WormGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_wheel_design(self) -> '_912.WormWheelDesign':
        '''WormWheelDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.WormWheelDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_straight_bevel_diff_gear_design(self) -> '_913.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_straight_bevel_gear_design(self) -> '_917.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.StraightBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_spiral_bevel_gear_design(self) -> '_921.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.SpiralBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_925.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_929.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_conical_gear_design(self) -> '_933.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_hypoid_gear_design(self) -> '_937.HypoidGearDesign':
        '''HypoidGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.HypoidGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_design(self) -> '_941.FaceGearDesign':
        '''FaceGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.FaceGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_pinion_design(self) -> '_946.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _946.FaceGearPinionDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_wheel_design(self) -> '_949.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _949.FaceGearWheelDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_design(self) -> '_964.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _964.CylindricalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_planet_gear_design(self) -> '_991.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _991.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_design(self) -> '_1096.ConicalGearDesign':
        '''ConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1096.ConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_concept_gear_design(self) -> '_1118.ConceptGearDesign':
        '''ConceptGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1118.ConceptGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_bevel_gear_design(self) -> '_1122.BevelGearDesign':
        '''BevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1122.BevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_agma_gleason_conical_gear_design(self) -> '_1135.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1135.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None
