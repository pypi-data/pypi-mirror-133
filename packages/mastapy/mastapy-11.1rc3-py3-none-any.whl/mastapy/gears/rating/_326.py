﻿'''_326.py

GearMeshRating
'''


from mastapy._internal import constructor
from mastapy.gears.load_case import _830
from mastapy.gears.load_case.worm import _833
from mastapy._internal.cast_exception import CastException
from mastapy.gears.load_case.face import _836
from mastapy.gears.load_case.cylindrical import _839
from mastapy.gears.load_case.conical import _842
from mastapy.gears.load_case.concept import _845
from mastapy.gears.load_case.bevel import _847
from mastapy.gears.rating import _319
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshRating',)


class GearMeshRating(_319.AbstractGearMeshRating):
    '''GearMeshRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_energy(self) -> 'float':
        '''float: 'TotalEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalEnergy

    @property
    def energy_loss(self) -> 'float':
        '''float: 'EnergyLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EnergyLoss

    @property
    def pinion_name(self) -> 'str':
        '''str: 'PinionName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionName

    @property
    def wheel_name(self) -> 'str':
        '''str: 'WheelName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelName

    @property
    def signed_pinion_torque(self) -> 'float':
        '''float: 'SignedPinionTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedPinionTorque

    @property
    def signed_wheel_torque(self) -> 'float':
        '''float: 'SignedWheelTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedWheelTorque

    @property
    def pinion_torque(self) -> 'float':
        '''float: 'PinionTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionTorque

    @property
    def wheel_torque(self) -> 'float':
        '''float: 'WheelTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelTorque

    @property
    def driving_gear(self) -> 'str':
        '''str: 'DrivingGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DrivingGear

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def mesh_efficiency(self) -> 'float':
        '''float: 'MeshEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshEfficiency

    @property
    def mesh_load_case(self) -> '_830.MeshLoadCase':
        '''MeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _830.MeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to MeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_worm_mesh_load_case(self) -> '_833.WormMeshLoadCase':
        '''WormMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _833.WormMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to WormMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_face_mesh_load_case(self) -> '_836.FaceMeshLoadCase':
        '''FaceMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _836.FaceMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to FaceMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_cylindrical_mesh_load_case(self) -> '_839.CylindricalMeshLoadCase':
        '''CylindricalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _839.CylindricalMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to CylindricalMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_conical_mesh_load_case(self) -> '_842.ConicalMeshLoadCase':
        '''ConicalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _842.ConicalMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to ConicalMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_concept_mesh_load_case(self) -> '_845.ConceptMeshLoadCase':
        '''ConceptMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _845.ConceptMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to ConceptMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None

    @property
    def mesh_load_case_of_type_bevel_mesh_load_case(self) -> '_847.BevelMeshLoadCase':
        '''BevelMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _847.BevelMeshLoadCase.TYPE not in self.wrapped.MeshLoadCase.__class__.__mro__:
            raise CastException('Failed to cast mesh_load_case to BevelMeshLoadCase. Expected: {}.'.format(self.wrapped.MeshLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshLoadCase.__class__)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase is not None else None
