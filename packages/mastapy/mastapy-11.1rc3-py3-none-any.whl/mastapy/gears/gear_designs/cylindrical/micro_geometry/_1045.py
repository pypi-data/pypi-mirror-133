'''_1045.py

CylindricalGearMeshMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _977, _971
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility_gui.charts import (
    _1621, _1612, _1617, _1618
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1052, _1047
from mastapy.gears.analysis import _1164
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMeshMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMicroGeometry',)


class CylindricalGearMeshMicroGeometry(_1164.GearMeshImplementationDetail):
    '''CylindricalGearMeshMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def profile_measured_as(self) -> '_977.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'ProfileMeasuredAs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileMeasuredAs)
        return constructor.new(_977.CylindricalGearProfileMeasurementType)(value) if value is not None else None

    @property
    def left_flank_lead_modification_chart(self) -> '_1621.TwoDChartDefinition':
        '''TwoDChartDefinition: 'LeftFlankLeadModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1621.TwoDChartDefinition.TYPE not in self.wrapped.LeftFlankLeadModificationChart.__class__.__mro__:
            raise CastException('Failed to cast left_flank_lead_modification_chart to TwoDChartDefinition. Expected: {}.'.format(self.wrapped.LeftFlankLeadModificationChart.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeftFlankLeadModificationChart.__class__)(self.wrapped.LeftFlankLeadModificationChart) if self.wrapped.LeftFlankLeadModificationChart is not None else None

    @property
    def right_flank_lead_modification_chart(self) -> '_1621.TwoDChartDefinition':
        '''TwoDChartDefinition: 'RightFlankLeadModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1621.TwoDChartDefinition.TYPE not in self.wrapped.RightFlankLeadModificationChart.__class__.__mro__:
            raise CastException('Failed to cast right_flank_lead_modification_chart to TwoDChartDefinition. Expected: {}.'.format(self.wrapped.RightFlankLeadModificationChart.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RightFlankLeadModificationChart.__class__)(self.wrapped.RightFlankLeadModificationChart) if self.wrapped.RightFlankLeadModificationChart is not None else None

    @property
    def left_flank_profile_modification_chart(self) -> '_1621.TwoDChartDefinition':
        '''TwoDChartDefinition: 'LeftFlankProfileModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1621.TwoDChartDefinition.TYPE not in self.wrapped.LeftFlankProfileModificationChart.__class__.__mro__:
            raise CastException('Failed to cast left_flank_profile_modification_chart to TwoDChartDefinition. Expected: {}.'.format(self.wrapped.LeftFlankProfileModificationChart.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeftFlankProfileModificationChart.__class__)(self.wrapped.LeftFlankProfileModificationChart) if self.wrapped.LeftFlankProfileModificationChart is not None else None

    @property
    def right_flank_profile_modification_chart(self) -> '_1621.TwoDChartDefinition':
        '''TwoDChartDefinition: 'RightFlankProfileModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1621.TwoDChartDefinition.TYPE not in self.wrapped.RightFlankProfileModificationChart.__class__.__mro__:
            raise CastException('Failed to cast right_flank_profile_modification_chart to TwoDChartDefinition. Expected: {}.'.format(self.wrapped.RightFlankProfileModificationChart.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RightFlankProfileModificationChart.__class__)(self.wrapped.RightFlankProfileModificationChart) if self.wrapped.RightFlankProfileModificationChart is not None else None

    @property
    def cylindrical_mesh(self) -> '_971.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'CylindricalMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_971.CylindricalGearMeshDesign)(self.wrapped.CylindricalMesh) if self.wrapped.CylindricalMesh is not None else None

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_1052.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1052.CylindricalGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry is not None else None

    @property
    def cylindrical_gear_micro_geometries(self) -> 'List[_1047.CylindricalGearMicroGeometry]':
        '''List[CylindricalGearMicroGeometry]: 'CylindricalGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMicroGeometries, constructor.new(_1047.CylindricalGearMicroGeometry))
        return value

    @property
    def gear_a(self) -> '_1047.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1047.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_b(self) -> '_1047.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1047.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB is not None else None
