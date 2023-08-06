﻿'''_2154.py

FELink
'''


from typing import List
from collections import OrderedDict

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item, overridable
from mastapy.system_model.fe import (
    _2134, _2138, _2100, _2133,
    _2121
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.dev_tools_analyses import _175
from mastapy.system_model.part_model import (
    _2181, _2173, _2174, _2177,
    _2179, _2184, _2185, _2188,
    _2189, _2191, _2198, _2199,
    _2200, _2202, _2205, _2207,
    _2208, _2213, _2215
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.part_model.gears import (
    _2248, _2250, _2252, _2253,
    _2254, _2256, _2258, _2260,
    _2262, _2263, _2265, _2269,
    _2271, _2273, _2275, _2278,
    _2280, _2282, _2284, _2285,
    _2286, _2288
)
from mastapy.system_model.part_model.cycloidal import _2304, _2305
from mastapy.system_model.part_model.couplings import (
    _2314, _2317, _2319, _2322,
    _2324, _2325, _2331, _2333,
    _2336, _2339, _2340, _2341,
    _2343, _2345
)
from mastapy.system_model.connections_and_sockets import (
    _2033, _2003, _2004, _2011,
    _2013, _2015, _2016, _2017,
    _2019, _2020, _2021, _2022,
    _2023, _2025, _2026, _2027,
    _2030, _2031
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2037, _2039, _2041, _2043,
    _2045, _2047, _2049, _2051,
    _2053, _2054, _2058, _2059,
    _2061, _2063, _2065, _2067,
    _2069
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2070, _2071, _2073, _2074,
    _2076, _2077
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2080, _2082, _2084, _2086,
    _2088, _2090, _2091
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'FELink')


__docformat__ = 'restructuredtext en'
__all__ = ('FELink',)


class FELink(_0.APIBase):
    '''FELink

    This is a mastapy class.
    '''

    TYPE = _FE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def external_node_ids(self) -> 'str':
        '''str: 'ExternalNodeIDs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExternalNodeIDs

    @property
    def component_name(self) -> 'str':
        '''str: 'ComponentName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ComponentName

    @property
    def connection(self) -> 'str':
        '''str: 'Connection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Connection

    @property
    def link_node_source(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource':
        '''enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource: 'LinkNodeSource' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.LinkNodeSource, value) if self.wrapped.LinkNodeSource is not None else None

    @link_node_source.setter
    def link_node_source(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LinkNodeSource = value

    @property
    def link_to_get_nodes_from(self) -> 'list_with_selected_item.ListWithSelectedItem_FELink':
        '''list_with_selected_item.ListWithSelectedItem_FELink: 'LinkToGetNodesFrom' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_FELink)(self.wrapped.LinkToGetNodesFrom) if self.wrapped.LinkToGetNodesFrom is not None else None

    @link_to_get_nodes_from.setter
    def link_to_get_nodes_from(self, value: 'list_with_selected_item.ListWithSelectedItem_FELink.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FELink.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FELink.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.LinkToGetNodesFrom = value

    @property
    def node_cylinder_search_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchDiameter) if self.wrapped.NodeCylinderSearchDiameter is not None else None

    @node_cylinder_search_diameter.setter
    def node_cylinder_search_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NodeCylinderSearchDiameter = value

    @property
    def node_cone_search_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeConeSearchAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeConeSearchAngle) if self.wrapped.NodeConeSearchAngle is not None else None

    @node_cone_search_angle.setter
    def node_cone_search_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NodeConeSearchAngle = value

    @property
    def node_search_cylinder_thickness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeSearchCylinderThickness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeSearchCylinderThickness) if self.wrapped.NodeSearchCylinderThickness is not None else None

    @node_search_cylinder_thickness.setter
    def node_search_cylinder_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NodeSearchCylinderThickness = value

    @property
    def node_cylinder_search_length(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchLength' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchLength) if self.wrapped.NodeCylinderSearchLength is not None else None

    @node_cylinder_search_length.setter
    def node_cylinder_search_length(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NodeCylinderSearchLength = value

    @property
    def node_cylinder_search_axial_offset(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchAxialOffset' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchAxialOffset) if self.wrapped.NodeCylinderSearchAxialOffset is not None else None

    @node_cylinder_search_axial_offset.setter
    def node_cylinder_search_axial_offset(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NodeCylinderSearchAxialOffset = value

    @property
    def number_of_nodes_in_ring(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfNodesInRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfNodesInRing) if self.wrapped.NumberOfNodesInRing is not None else None

    @number_of_nodes_in_ring.setter
    def number_of_nodes_in_ring(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfNodesInRing = value

    @property
    def has_teeth(self) -> 'bool':
        '''bool: 'HasTeeth' is the original name of this property.'''

        return self.wrapped.HasTeeth

    @has_teeth.setter
    def has_teeth(self, value: 'bool'):
        self.wrapped.HasTeeth = bool(value) if value else False

    @property
    def angle_of_centre_of_connection_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AngleOfCentreOfConnectionPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AngleOfCentreOfConnectionPatch) if self.wrapped.AngleOfCentreOfConnectionPatch is not None else None

    @angle_of_centre_of_connection_patch.setter
    def angle_of_centre_of_connection_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AngleOfCentreOfConnectionPatch = value

    @property
    def span_of_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpanOfPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpanOfPatch) if self.wrapped.SpanOfPatch is not None else None

    @span_of_patch.setter
    def span_of_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpanOfPatch = value

    @property
    def node_selection_depth(self) -> 'overridable.Overridable_NodeSelectionDepthOption':
        '''overridable.Overridable_NodeSelectionDepthOption: 'NodeSelectionDepth' is the original name of this property.'''

        value = overridable.Overridable_NodeSelectionDepthOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.NodeSelectionDepth, value) if self.wrapped.NodeSelectionDepth is not None else None

    @node_selection_depth.setter
    def node_selection_depth(self, value: 'overridable.Overridable_NodeSelectionDepthOption.implicit_type()'):
        wrapper_type = overridable.Overridable_NodeSelectionDepthOption.wrapper_type()
        enclosed_type = overridable.Overridable_NodeSelectionDepthOption.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.NodeSelectionDepth = value

    @property
    def coupling_type(self) -> 'overridable.Overridable_RigidCouplingType':
        '''overridable.Overridable_RigidCouplingType: 'CouplingType' is the original name of this property.'''

        value = overridable.Overridable_RigidCouplingType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.CouplingType, value) if self.wrapped.CouplingType is not None else None

    @coupling_type.setter
    def coupling_type(self, value: 'overridable.Overridable_RigidCouplingType.implicit_type()'):
        wrapper_type = overridable.Overridable_RigidCouplingType.wrapper_type()
        enclosed_type = overridable.Overridable_RigidCouplingType.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.CouplingType = value

    @property
    def number_of_axial_nodes(self) -> 'int':
        '''int: 'NumberOfAxialNodes' is the original name of this property.'''

        return self.wrapped.NumberOfAxialNodes

    @number_of_axial_nodes.setter
    def number_of_axial_nodes(self, value: 'int'):
        self.wrapped.NumberOfAxialNodes = int(value) if value else 0

    @property
    def bearing_node_link_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingNodeOption':
        '''enum_with_selected_value.EnumWithSelectedValue_BearingNodeOption: 'BearingNodeLinkOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_BearingNodeOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.BearingNodeLinkOption, value) if self.wrapped.BearingNodeLinkOption is not None else None

    @bearing_node_link_option.setter
    def bearing_node_link_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingNodeOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingNodeOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BearingNodeLinkOption = value

    @property
    def width_of_axial_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'WidthOfAxialPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.WidthOfAxialPatch) if self.wrapped.WidthOfAxialPatch is not None else None

    @width_of_axial_patch.setter
    def width_of_axial_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WidthOfAxialPatch = value

    @property
    def connect_to_midside_nodes(self) -> 'bool':
        '''bool: 'ConnectToMidsideNodes' is the original name of this property.'''

        return self.wrapped.ConnectToMidsideNodes

    @connect_to_midside_nodes.setter
    def connect_to_midside_nodes(self, value: 'bool'):
        self.wrapped.ConnectToMidsideNodes = bool(value) if value else False

    @property
    def bearing_race_in_fe(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'BearingRaceInFE' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.BearingRaceInFE) if self.wrapped.BearingRaceInFE is not None else None

    @bearing_race_in_fe.setter
    def bearing_race_in_fe(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.BearingRaceInFE = value

    @property
    def number_of_nodes_in_full_fe_mesh(self) -> 'int':
        '''int: 'NumberOfNodesInFullFEMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfNodesInFullFEMesh

    @property
    def component(self) -> '_2181.Component':
        '''Component: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.Component.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Component. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_abstract_shaft(self) -> '_2173.AbstractShaft':
        '''AbstractShaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.AbstractShaft.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AbstractShaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_abstract_shaft_or_housing(self) -> '_2174.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.AbstractShaftOrHousing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bearing(self) -> '_2177.Bearing':
        '''Bearing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.Bearing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bearing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bolt(self) -> '_2179.Bolt':
        '''Bolt: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.Bolt.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bolt. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_connector(self) -> '_2184.Connector':
        '''Connector: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2184.Connector.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Connector. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_datum(self) -> '_2185.Datum':
        '''Datum: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Datum.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Datum. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_external_cad_model(self) -> '_2188.ExternalCADModel':
        '''ExternalCADModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.ExternalCADModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ExternalCADModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_fe_part(self) -> '_2189.FEPart':
        '''FEPart: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.FEPart.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to FEPart. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_guide_dxf_model(self) -> '_2191.GuideDxfModel':
        '''GuideDxfModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.GuideDxfModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to GuideDxfModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_mass_disc(self) -> '_2198.MassDisc':
        '''MassDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.MassDisc.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MassDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_measurement_component(self) -> '_2199.MeasurementComponent':
        '''MeasurementComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.MeasurementComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MeasurementComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_mountable_component(self) -> '_2200.MountableComponent':
        '''MountableComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.MountableComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MountableComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_oil_seal(self) -> '_2202.OilSeal':
        '''OilSeal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2202.OilSeal.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to OilSeal. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_planet_carrier(self) -> '_2205.PlanetCarrier':
        '''PlanetCarrier: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2205.PlanetCarrier.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PlanetCarrier. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_point_load(self) -> '_2207.PointLoad':
        '''PointLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.PointLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PointLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_power_load(self) -> '_2208.PowerLoad':
        '''PowerLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.PowerLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PowerLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_unbalanced_mass(self) -> '_2213.UnbalancedMass':
        '''UnbalancedMass: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.UnbalancedMass.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to UnbalancedMass. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_virtual_component(self) -> '_2215.VirtualComponent':
        '''VirtualComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.VirtualComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to VirtualComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_shaft(self) -> '_2218.Shaft':
        '''Shaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.Shaft.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Shaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_agma_gleason_conical_gear(self) -> '_2248.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.AGMAGleasonConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bevel_differential_gear(self) -> '_2250.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.BevelDifferentialGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bevel_differential_planet_gear(self) -> '_2252.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bevel_differential_sun_gear(self) -> '_2253.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.BevelDifferentialSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_bevel_gear(self) -> '_2254.BevelGear':
        '''BevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.BevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_concept_gear(self) -> '_2256.ConceptGear':
        '''ConceptGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.ConceptGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_conical_gear(self) -> '_2258.ConicalGear':
        '''ConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.ConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_cylindrical_gear(self) -> '_2260.CylindricalGear':
        '''CylindricalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.CylindricalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_cylindrical_planet_gear(self) -> '_2262.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.CylindricalPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_face_gear(self) -> '_2263.FaceGear':
        '''FaceGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.FaceGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to FaceGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_gear(self) -> '_2265.Gear':
        '''Gear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Gear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Gear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_hypoid_gear(self) -> '_2269.HypoidGear':
        '''HypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2269.HypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to HypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2271.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2273.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2275.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2275.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_spiral_bevel_gear(self) -> '_2278.SpiralBevelGear':
        '''SpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2278.SpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_straight_bevel_diff_gear(self) -> '_2280.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2280.StraightBevelDiffGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_straight_bevel_gear(self) -> '_2282.StraightBevelGear':
        '''StraightBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.StraightBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_straight_bevel_planet_gear(self) -> '_2284.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2284.StraightBevelPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_straight_bevel_sun_gear(self) -> '_2285.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.StraightBevelSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_worm_gear(self) -> '_2286.WormGear':
        '''WormGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.WormGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to WormGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_zerol_bevel_gear(self) -> '_2288.ZerolBevelGear':
        '''ZerolBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.ZerolBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_cycloidal_disc(self) -> '_2304.CycloidalDisc':
        '''CycloidalDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.CycloidalDisc.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CycloidalDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_ring_pins(self) -> '_2305.RingPins':
        '''RingPins: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.RingPins.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to RingPins. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_clutch_half(self) -> '_2314.ClutchHalf':
        '''ClutchHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.ClutchHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ClutchHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_concept_coupling_half(self) -> '_2317.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.ConceptCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_coupling_half(self) -> '_2319.CouplingHalf':
        '''CouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.CouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_cvt_pulley(self) -> '_2322.CVTPulley':
        '''CVTPulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.CVTPulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CVTPulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_part_to_part_shear_coupling_half(self) -> '_2324.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2324.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_pulley(self) -> '_2325.Pulley':
        '''Pulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.Pulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Pulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_rolling_ring(self) -> '_2331.RollingRing':
        '''RollingRing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2331.RollingRing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to RollingRing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_shaft_hub_connection(self) -> '_2333.ShaftHubConnection':
        '''ShaftHubConnection: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.ShaftHubConnection.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_spring_damper_half(self) -> '_2336.SpringDamperHalf':
        '''SpringDamperHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2336.SpringDamperHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_synchroniser_half(self) -> '_2339.SynchroniserHalf':
        '''SynchroniserHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.SynchroniserHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_synchroniser_part(self) -> '_2340.SynchroniserPart':
        '''SynchroniserPart: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2340.SynchroniserPart.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserPart. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_synchroniser_sleeve(self) -> '_2341.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.SynchroniserSleeve.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_torque_converter_pump(self) -> '_2343.TorqueConverterPump':
        '''TorqueConverterPump: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2343.TorqueConverterPump.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def component_of_type_torque_converter_turbine(self) -> '_2345.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2345.TorqueConverterTurbine.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Component.__class__)(self.wrapped.Component) if self.wrapped.Component is not None else None

    @property
    def socket(self) -> '_2033.Socket':
        '''Socket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.Socket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to Socket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_bearing_inner_socket(self) -> '_2003.BearingInnerSocket':
        '''BearingInnerSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.BearingInnerSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_bearing_outer_socket(self) -> '_2004.BearingOuterSocket':
        '''BearingOuterSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.BearingOuterSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cvt_pulley_socket(self) -> '_2011.CVTPulleySocket':
        '''CVTPulleySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.CVTPulleySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cylindrical_socket(self) -> '_2013.CylindricalSocket':
        '''CylindricalSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CylindricalSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_electric_machine_stator_socket(self) -> '_2015.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.ElectricMachineStatorSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_inner_shaft_socket(self) -> '_2016.InnerShaftSocket':
        '''InnerShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.InnerShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_inner_shaft_socket_base(self) -> '_2017.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.InnerShaftSocketBase.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_mountable_component_inner_socket(self) -> '_2019.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.MountableComponentInnerSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_mountable_component_outer_socket(self) -> '_2020.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.MountableComponentOuterSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_mountable_component_socket(self) -> '_2021.MountableComponentSocket':
        '''MountableComponentSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.MountableComponentSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_outer_shaft_socket(self) -> '_2022.OuterShaftSocket':
        '''OuterShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.OuterShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_outer_shaft_socket_base(self) -> '_2023.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.OuterShaftSocketBase.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_planetary_socket(self) -> '_2025.PlanetarySocket':
        '''PlanetarySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.PlanetarySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_planetary_socket_base(self) -> '_2026.PlanetarySocketBase':
        '''PlanetarySocketBase: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.PlanetarySocketBase.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_pulley_socket(self) -> '_2027.PulleySocket':
        '''PulleySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.PulleySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PulleySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_rolling_ring_socket(self) -> '_2030.RollingRingSocket':
        '''RollingRingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.RollingRingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_shaft_socket(self) -> '_2031.ShaftSocket':
        '''ShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.ShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2037.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_bevel_differential_gear_teeth_socket(self) -> '_2039.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_bevel_gear_teeth_socket(self) -> '_2041.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.BevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_concept_gear_teeth_socket(self) -> '_2043.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.ConceptGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_conical_gear_teeth_socket(self) -> '_2045.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.ConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2047.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.CylindricalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_face_gear_teeth_socket(self) -> '_2049.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.FaceGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_gear_teeth_socket(self) -> '_2051.GearTeethSocket':
        '''GearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.GearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to GearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_hypoid_gear_teeth_socket(self) -> '_2053.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.HypoidGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2054.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2058.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2059.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2061.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2063.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_straight_bevel_gear_teeth_socket(self) -> '_2065.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_worm_gear_teeth_socket(self) -> '_2067.WormGearTeethSocket':
        '''WormGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2069.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2070.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2071.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cycloidal_disc_inner_socket(self) -> '_2073.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.CycloidalDiscInnerSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cycloidal_disc_outer_socket(self) -> '_2074.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.CycloidalDiscOuterSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2076.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_ring_pins_socket(self) -> '_2077.RingPinsSocket':
        '''RingPinsSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.RingPinsSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_clutch_socket(self) -> '_2080.ClutchSocket':
        '''ClutchSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.ClutchSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ClutchSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_concept_coupling_socket(self) -> '_2082.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptCouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_coupling_socket(self) -> '_2084.CouplingSocket':
        '''CouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.CouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2086.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.PartToPartShearCouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_spring_damper_socket(self) -> '_2088.SpringDamperSocket':
        '''SpringDamperSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.SpringDamperSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_torque_converter_pump_socket(self) -> '_2090.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.TorqueConverterPumpSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def socket_of_type_torque_converter_turbine_socket(self) -> '_2091.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.TorqueConverterTurbineSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Socket.__class__)(self.wrapped.Socket) if self.wrapped.Socket is not None else None

    @property
    def alignment_in_world_coordinate_system(self) -> '_2133.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInWorldCoordinateSystem) if self.wrapped.AlignmentInWorldCoordinateSystem is not None else None

    @property
    def alignment_in_fe_coordinate_system(self) -> '_2133.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInFECoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInFECoordinateSystem) if self.wrapped.AlignmentInFECoordinateSystem is not None else None

    @property
    def alignment_in_component_coordinate_system(self) -> '_2133.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInComponentCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInComponentCoordinateSystem) if self.wrapped.AlignmentInComponentCoordinateSystem is not None else None

    @property
    def nodes(self) -> 'List[_2121.FESubstructureNode]':
        '''List[FESubstructureNode]: 'Nodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Nodes, constructor.new(_2121.FESubstructureNode))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    def nodes_grouped_by_angle(self) -> 'OrderedDict[float, List[_2121.FESubstructureNode]]':
        ''' 'NodesGroupedByAngle' is the original name of this method.

        Returns:
            OrderedDict[float, List[mastapy.system_model.fe.FESubstructureNode]]
        '''

        return conversion.pn_to_mp_objects_in_list_in_ordered_dict(self.wrapped.NodesGroupedByAngle(), constructor.new(_2121.FESubstructureNode))

    def remove_all_nodes(self):
        ''' 'RemoveAllNodes' is the original name of this method.'''

        self.wrapped.RemoveAllNodes()

    def add_or_replace_node(self, node: '_2121.FESubstructureNode'):
        ''' 'AddOrReplaceNode' is the original name of this method.

        Args:
            node (mastapy.system_model.fe.FESubstructureNode)
        '''

        self.wrapped.AddOrReplaceNode(node.wrapped if node else None)

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
