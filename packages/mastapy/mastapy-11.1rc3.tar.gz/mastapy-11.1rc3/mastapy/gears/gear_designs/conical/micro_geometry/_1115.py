﻿'''_1115.py

ConicalGearFlankMicroGeometry
'''


from mastapy.gears import _302
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.conical.micro_geometry import _1117, _1116, _1114
from mastapy.gears.gear_designs.conical import _1096
from mastapy.gears.gear_designs.zerol_bevel import _904
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _913
from mastapy.gears.gear_designs.straight_bevel import _917
from mastapy.gears.gear_designs.spiral_bevel import _921
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _925
from mastapy.gears.gear_designs.klingelnberg_hypoid import _929
from mastapy.gears.gear_designs.klingelnberg_conical import _933
from mastapy.gears.gear_designs.hypoid import _937
from mastapy.gears.gear_designs.bevel import _1122
from mastapy.gears.gear_designs.agma_gleason_conical import _1135
from mastapy.gears.micro_geometry import _525
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry', 'ConicalGearFlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearFlankMicroGeometry',)


class ConicalGearFlankMicroGeometry(_525.FlankMicroGeometry):
    '''ConicalGearFlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearFlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def micro_geometry_input_type(self) -> '_302.MicroGeometryInputTypes':
        '''MicroGeometryInputTypes: 'MicroGeometryInputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MicroGeometryInputType)
        return constructor.new(_302.MicroGeometryInputTypes)(value) if value is not None else None

    @micro_geometry_input_type.setter
    def micro_geometry_input_type(self, value: '_302.MicroGeometryInputTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryInputType = value

    @property
    def profile_relief(self) -> '_1117.ConicalGearProfileModification':
        '''ConicalGearProfileModification: 'ProfileRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1117.ConicalGearProfileModification)(self.wrapped.ProfileRelief) if self.wrapped.ProfileRelief is not None else None

    @property
    def lead_relief(self) -> '_1116.ConicalGearLeadModification':
        '''ConicalGearLeadModification: 'LeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1116.ConicalGearLeadModification)(self.wrapped.LeadRelief) if self.wrapped.LeadRelief is not None else None

    @property
    def bias(self) -> '_1114.ConicalGearBiasModification':
        '''ConicalGearBiasModification: 'Bias' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1114.ConicalGearBiasModification)(self.wrapped.Bias) if self.wrapped.Bias is not None else None

    @property
    def gear_design(self) -> '_1096.ConicalGearDesign':
        '''ConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1096.ConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_zerol_bevel_gear_design(self) -> '_904.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.ZerolBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_913.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_straight_bevel_gear_design(self) -> '_917.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.StraightBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_spiral_bevel_gear_design(self) -> '_921.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.SpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_925.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_929.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_933.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_hypoid_gear_design(self) -> '_937.HypoidGearDesign':
        '''HypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.HypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_bevel_gear_design(self) -> '_1122.BevelGearDesign':
        '''BevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1122.BevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_1135.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1135.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None
