'''list_with_selected_item.py

Implementations of 'ListWithSelectedItem' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from typing import List, Generic, TypeVar

from mastapy._internal import mixins, constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.ltca.cylindrical import _812, _811
from mastapy.gears.manufacturing.cylindrical import _580
from mastapy.gears.manufacturing.bevel import _746
from mastapy.utility import _1388
from mastapy.utility.units_and_measurements import (
    _1398, _1390, _1391, _1392,
    _1396, _1397, _1399, _1393
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility.units_and_measurements.measurements import (
    _1400, _1401, _1402, _1403,
    _1404, _1405, _1406, _1407,
    _1408, _1409, _1410, _1411,
    _1412, _1413, _1414, _1415,
    _1416, _1417, _1418, _1419,
    _1420, _1421, _1422, _1423,
    _1424, _1425, _1426, _1427,
    _1428, _1429, _1430, _1431,
    _1432, _1433, _1434, _1435,
    _1436, _1437, _1438, _1439,
    _1440, _1441, _1442, _1443,
    _1444, _1445, _1446, _1447,
    _1448, _1449, _1450, _1451,
    _1452, _1453, _1454, _1455,
    _1456, _1457, _1458, _1459,
    _1460, _1461, _1462, _1463,
    _1464, _1465, _1466, _1467,
    _1468, _1469, _1470, _1471,
    _1472, _1473, _1474, _1475,
    _1476, _1477, _1478, _1479,
    _1480, _1481, _1482, _1483,
    _1484, _1485, _1486, _1487,
    _1488, _1489, _1490, _1491,
    _1492, _1493, _1494, _1495,
    _1496, _1497, _1498, _1499,
    _1500, _1501, _1502, _1503,
    _1504, _1505, _1506, _1507
)
from mastapy.utility.file_access_helpers import _1581
from mastapy.system_model.part_model import (
    _2208, _2185, _2181, _2173,
    _2174, _2177, _2179, _2184,
    _2188, _2189, _2191, _2198,
    _2199, _2200, _2202, _2205,
    _2207, _2213, _2215
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5658, _5711, _5712, _5713,
    _5714, _5715, _5716, _5717,
    _5718, _5719, _5720, _5721,
    _5731, _5733, _5734, _5736,
    _5765, _5781, _5806
)
from mastapy._internal.tuple_with_name import TupleWithName
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2489, _2424, _2431, _2436,
    _2450, _2454, _2469, _2470,
    _2471, _2484, _2493, _2498,
    _2501, _2504, _2537, _2543,
    _2546, _2566, _2569, _2475,
    _2476, _2477, _2480
)
from mastapy.system_model.part_model.gears import (
    _2267, _2249, _2251, _2255,
    _2257, _2259, _2261, _2264,
    _2270, _2272, _2274, _2276,
    _2277, _2279, _2281, _2283,
    _2287, _2289, _2248, _2250,
    _2252, _2253, _2254, _2256,
    _2258, _2260, _2262, _2263,
    _2265, _2269, _2271, _2273,
    _2275, _2278, _2280, _2282,
    _2284, _2285, _2286, _2288
)
from mastapy.system_model.fe import _2121, _2119, _2110
from mastapy.system_model.part_model.shaft_model import _2218
from mastapy.system_model.part_model.cycloidal import _2304, _2305
from mastapy.system_model.part_model.couplings import (
    _2314, _2317, _2319, _2322,
    _2324, _2325, _2331, _2333,
    _2336, _2339, _2340, _2341,
    _2343, _2345
)
from mastapy.system_model.fe.links import (
    _2154, _2155, _2157, _2158,
    _2159, _2160, _2161, _2162,
    _2163, _2164, _2165, _2166,
    _2167, _2168
)
from mastapy.system_model.part_model.part_groups import _2223
from mastapy.gears.gear_designs import _902
from mastapy.gears.gear_designs.zerol_bevel import _906
from mastapy.gears.gear_designs.worm import _911
from mastapy.gears.gear_designs.straight_bevel_diff import _915
from mastapy.gears.gear_designs.straight_bevel import _919
from mastapy.gears.gear_designs.spiral_bevel import _923
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _927
from mastapy.gears.gear_designs.klingelnberg_hypoid import _931
from mastapy.gears.gear_designs.klingelnberg_conical import _935
from mastapy.gears.gear_designs.hypoid import _939
from mastapy.gears.gear_designs.face import _947
from mastapy.gears.gear_designs.cylindrical import _979, _990
from mastapy.gears.gear_designs.conical import _1098
from mastapy.gears.gear_designs.concept import _1120
from mastapy.gears.gear_designs.bevel import _1124
from mastapy.gears.gear_designs.agma_gleason_conical import _1137
from mastapy.system_model.analyses_and_results.load_case_groups import _5383, _5384
from mastapy.system_model.analyses_and_results.harmonic_analyses.results import _5822
from mastapy.system_model.analyses_and_results.static_loads import _6514, _6521
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4113

_ARRAY = python_net_import('System', 'Array')
_LIST_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.Utility.Property', 'ListWithSelectedItem')


__docformat__ = 'restructuredtext en'
__all__ = (
    'ListWithSelectedItem_str', 'ListWithSelectedItem_int',
    'ListWithSelectedItem_T', 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis',
    'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis', 'ListWithSelectedItem_CylindricalSetManufacturingConfig',
    'ListWithSelectedItem_ConicalSetManufacturingConfig', 'ListWithSelectedItem_SystemDirectory',
    'ListWithSelectedItem_Unit', 'ListWithSelectedItem_MeasurementBase',
    'ListWithSelectedItem_ColumnTitle', 'ListWithSelectedItem_PowerLoad',
    'ListWithSelectedItem_AbstractPeriodicExcitationDetail', 'ListWithSelectedItem_TupleWithName',
    'ListWithSelectedItem_GearMeshSystemDeflection', 'ListWithSelectedItem_GearSet',
    'ListWithSelectedItem_FESubstructureNode', 'ListWithSelectedItem_Datum',
    'ListWithSelectedItem_Component', 'ListWithSelectedItem_FELink',
    'ListWithSelectedItem_FESubstructure', 'ListWithSelectedItem_CylindricalGear',
    'ListWithSelectedItem_GuideDxfModel', 'ListWithSelectedItem_ConcentricPartGroup',
    'ListWithSelectedItem_CylindricalGearSet', 'ListWithSelectedItem_GearSetDesign',
    'ListWithSelectedItem_ShaftHubConnection', 'ListWithSelectedItem_TSelectableItem',
    'ListWithSelectedItem_CylindricalGearSystemDeflection', 'ListWithSelectedItem_DesignState',
    'ListWithSelectedItem_FEPart', 'ListWithSelectedItem_TPartAnalysis',
    'ListWithSelectedItem_ResultLocationSelectionGroup', 'ListWithSelectedItem_StaticLoadCase',
    'ListWithSelectedItem_DutyCycle', 'ListWithSelectedItem_float',
    'ListWithSelectedItem_ElectricMachineDataSet', 'ListWithSelectedItem_PointLoad'
)


T = TypeVar('T')
TSelectableItem = TypeVar('TSelectableItem')
TPartAnalysis = TypeVar('TPartAnalysis')


class ListWithSelectedItem_str(str, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_str

    A specific implementation of 'ListWithSelectedItem' for 'str' types.
    '''

    __hash__ = None
    __qualname__ = 'str'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        return str.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else '')

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'str':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return str

    @property
    def selected_value(self) -> 'str':
        '''str: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[str]':
        '''List[str]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, str)
        return value


class ListWithSelectedItem_int(int, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_int

    A specific implementation of 'ListWithSelectedItem' for 'int' types.
    '''

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else 0)

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def selected_value(self) -> 'int':
        '''int: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[int]':
        '''List[int]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, int)
        return value


class ListWithSelectedItem_T(Generic[T], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_T

    A specific implementation of 'ListWithSelectedItem' for 'T' types.
    '''

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def selected_value(self) -> 'T':
        '''T: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[T]':
        '''List[T]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis(_812.CylindricalGearMeshLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearMeshLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearMeshLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_812.CylindricalGearMeshLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _812.CylindricalGearMeshLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_812.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_812.CylindricalGearMeshLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_812.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_812.CylindricalGearMeshLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis(_811.CylindricalGearLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_811.CylindricalGearLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _811.CylindricalGearLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_811.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_811.CylindricalGearLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_811.CylindricalGearLoadDistributionAnalysis]':
        '''List[CylindricalGearLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_811.CylindricalGearLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalSetManufacturingConfig(_580.CylindricalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_580.CylindricalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _580.CylindricalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_580.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_580.CylindricalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_580.CylindricalSetManufacturingConfig]':
        '''List[CylindricalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_580.CylindricalSetManufacturingConfig))
        return value


class ListWithSelectedItem_ConicalSetManufacturingConfig(_746.ConicalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConicalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'ConicalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConicalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_746.ConicalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _746.ConicalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_746.ConicalSetManufacturingConfig':
        '''ConicalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_746.ConicalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_746.ConicalSetManufacturingConfig]':
        '''List[ConicalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_746.ConicalSetManufacturingConfig))
        return value


class ListWithSelectedItem_SystemDirectory(_1388.SystemDirectory, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_SystemDirectory

    A specific implementation of 'ListWithSelectedItem' for 'SystemDirectory' types.
    '''

    __hash__ = None
    __qualname__ = 'SystemDirectory'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_SystemDirectory.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1388.SystemDirectory.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1388.SystemDirectory.TYPE

    @property
    def selected_value(self) -> '_1388.SystemDirectory':
        '''SystemDirectory: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1388.SystemDirectory)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1388.SystemDirectory]':
        '''List[SystemDirectory]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1388.SystemDirectory))
        return value


class ListWithSelectedItem_Unit(_1398.Unit, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Unit

    A specific implementation of 'ListWithSelectedItem' for 'Unit' types.
    '''

    __hash__ = None
    __qualname__ = 'Unit'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Unit.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1398.Unit.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1398.Unit.TYPE

    @property
    def selected_value(self) -> '_1398.Unit':
        '''Unit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1398.Unit.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Unit. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1398.Unit]':
        '''List[Unit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1398.Unit))
        return value


class ListWithSelectedItem_MeasurementBase(_1393.MeasurementBase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_MeasurementBase

    A specific implementation of 'ListWithSelectedItem' for 'MeasurementBase' types.
    '''

    __hash__ = None
    __qualname__ = 'MeasurementBase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_MeasurementBase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1393.MeasurementBase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1393.MeasurementBase.TYPE

    @property
    def selected_value(self) -> '_1393.MeasurementBase':
        '''MeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1393.MeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_acceleration(self) -> '_1400.Acceleration':
        '''Acceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1400.Acceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Acceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle(self) -> '_1401.Angle':
        '''Angle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1401.Angle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Angle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_per_unit_temperature(self) -> '_1402.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1402.AnglePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AnglePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_small(self) -> '_1403.AngleSmall':
        '''AngleSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1403.AngleSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_very_small(self) -> '_1404.AngleVerySmall':
        '''AngleVerySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1404.AngleVerySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleVerySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_acceleration(self) -> '_1405.AngularAcceleration':
        '''AngularAcceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1405.AngularAcceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularAcceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_compliance(self) -> '_1406.AngularCompliance':
        '''AngularCompliance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1406.AngularCompliance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularCompliance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_jerk(self) -> '_1407.AngularJerk':
        '''AngularJerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1407.AngularJerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularJerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_stiffness(self) -> '_1408.AngularStiffness':
        '''AngularStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1408.AngularStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_velocity(self) -> '_1409.AngularVelocity':
        '''AngularVelocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1409.AngularVelocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularVelocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_area(self) -> '_1410.Area':
        '''Area: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1410.Area.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Area. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_area_small(self) -> '_1411.AreaSmall':
        '''AreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1411.AreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cycles(self) -> '_1412.Cycles':
        '''Cycles: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1412.Cycles.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Cycles. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_damage(self) -> '_1413.Damage':
        '''Damage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1413.Damage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Damage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_damage_rate(self) -> '_1414.DamageRate':
        '''DamageRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1414.DamageRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DamageRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_data_size(self) -> '_1415.DataSize':
        '''DataSize: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1415.DataSize.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DataSize. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_decibel(self) -> '_1416.Decibel':
        '''Decibel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1416.Decibel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Decibel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_density(self) -> '_1417.Density':
        '''Density: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1417.Density.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Density. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy(self) -> '_1418.Energy':
        '''Energy: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1418.Energy.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Energy. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_per_unit_area(self) -> '_1419.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1419.EnergyPerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_per_unit_area_small(self) -> '_1420.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1420.EnergyPerUnitAreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_small(self) -> '_1421.EnergySmall':
        '''EnergySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1421.EnergySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_enum(self) -> '_1422.Enum':
        '''Enum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1422.Enum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Enum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_flow_rate(self) -> '_1423.FlowRate':
        '''FlowRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1423.FlowRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FlowRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force(self) -> '_1424.Force':
        '''Force: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1424.Force.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Force. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_length(self) -> '_1425.ForcePerUnitLength':
        '''ForcePerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1425.ForcePerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_pressure(self) -> '_1426.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1426.ForcePerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_temperature(self) -> '_1427.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1427.ForcePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fraction_measurement_base(self) -> '_1428.FractionMeasurementBase':
        '''FractionMeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1428.FractionMeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FractionMeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_frequency(self) -> '_1429.Frequency':
        '''Frequency: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1429.Frequency.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Frequency. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fuel_consumption_engine(self) -> '_1430.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1430.FuelConsumptionEngine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelConsumptionEngine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fuel_efficiency_vehicle(self) -> '_1431.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1431.FuelEfficiencyVehicle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelEfficiencyVehicle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gradient(self) -> '_1432.Gradient':
        '''Gradient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1432.Gradient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gradient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_conductivity(self) -> '_1433.HeatConductivity':
        '''HeatConductivity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1433.HeatConductivity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatConductivity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer(self) -> '_1434.HeatTransfer':
        '''HeatTransfer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1434.HeatTransfer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransfer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1435.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1435.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer_resistance(self) -> '_1436.HeatTransferResistance':
        '''HeatTransferResistance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1436.HeatTransferResistance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferResistance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_impulse(self) -> '_1437.Impulse':
        '''Impulse: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1437.Impulse.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Impulse. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_index(self) -> '_1438.Index':
        '''Index: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1438.Index.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Index. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_integer(self) -> '_1439.Integer':
        '''Integer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1439.Integer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Integer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_inverse_short_length(self) -> '_1440.InverseShortLength':
        '''InverseShortLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1440.InverseShortLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_inverse_short_time(self) -> '_1441.InverseShortTime':
        '''InverseShortTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1441.InverseShortTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_jerk(self) -> '_1442.Jerk':
        '''Jerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1442.Jerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Jerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_kinematic_viscosity(self) -> '_1443.KinematicViscosity':
        '''KinematicViscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1443.KinematicViscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KinematicViscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_long(self) -> '_1444.LengthLong':
        '''LengthLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1444.LengthLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_medium(self) -> '_1445.LengthMedium':
        '''LengthMedium: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1445.LengthMedium.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthMedium. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_per_unit_temperature(self) -> '_1446.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1446.LengthPerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthPerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_short(self) -> '_1447.LengthShort':
        '''LengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1447.LengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_to_the_fourth(self) -> '_1448.LengthToTheFourth':
        '''LengthToTheFourth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1448.LengthToTheFourth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthToTheFourth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_long(self) -> '_1449.LengthVeryLong':
        '''LengthVeryLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1449.LengthVeryLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_short(self) -> '_1450.LengthVeryShort':
        '''LengthVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1450.LengthVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_short_per_length_short(self) -> '_1451.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1451.LengthVeryShortPerLengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_angular_damping(self) -> '_1452.LinearAngularDamping':
        '''LinearAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1452.LinearAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_angular_stiffness_cross_term(self) -> '_1453.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1453.LinearAngularStiffnessCrossTerm.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_damping(self) -> '_1454.LinearDamping':
        '''LinearDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1454.LinearDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_flexibility(self) -> '_1455.LinearFlexibility':
        '''LinearFlexibility: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1455.LinearFlexibility.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearFlexibility. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_stiffness(self) -> '_1456.LinearStiffness':
        '''LinearStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1456.LinearStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass(self) -> '_1457.Mass':
        '''Mass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1457.Mass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Mass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_per_unit_length(self) -> '_1458.MassPerUnitLength':
        '''MassPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1458.MassPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_per_unit_time(self) -> '_1459.MassPerUnitTime':
        '''MassPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1459.MassPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_of_inertia(self) -> '_1460.MomentOfInertia':
        '''MomentOfInertia: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1460.MomentOfInertia.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertia. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_of_inertia_per_unit_length(self) -> '_1461.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1461.MomentOfInertiaPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_per_unit_pressure(self) -> '_1462.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1462.MomentPerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentPerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_number(self) -> '_1463.Number':
        '''Number: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1463.Number.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Number. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_percentage(self) -> '_1464.Percentage':
        '''Percentage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1464.Percentage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Percentage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power(self) -> '_1465.Power':
        '''Power: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1465.Power.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Power. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_per_small_area(self) -> '_1466.PowerPerSmallArea':
        '''PowerPerSmallArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1466.PowerPerSmallArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerSmallArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_per_unit_time(self) -> '_1467.PowerPerUnitTime':
        '''PowerPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1467.PowerPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small(self) -> '_1468.PowerSmall':
        '''PowerSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1468.PowerSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_area(self) -> '_1469.PowerSmallPerArea':
        '''PowerSmallPerArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1469.PowerSmallPerArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1470.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1470.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_unit_time(self) -> '_1471.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1471.PowerSmallPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure(self) -> '_1472.Pressure':
        '''Pressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1472.Pressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_per_unit_time(self) -> '_1473.PressurePerUnitTime':
        '''PressurePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1473.PressurePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressurePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_velocity_product(self) -> '_1474.PressureVelocityProduct':
        '''PressureVelocityProduct: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1474.PressureVelocityProduct.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureVelocityProduct. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_viscosity_coefficient(self) -> '_1475.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1475.PressureViscosityCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureViscosityCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_price(self) -> '_1476.Price':
        '''Price: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1476.Price.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Price. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_quadratic_angular_damping(self) -> '_1477.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1477.QuadraticAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_quadratic_drag(self) -> '_1478.QuadraticDrag':
        '''QuadraticDrag: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1478.QuadraticDrag.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticDrag. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rescaled_measurement(self) -> '_1479.RescaledMeasurement':
        '''RescaledMeasurement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1479.RescaledMeasurement.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RescaledMeasurement. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rotatum(self) -> '_1480.Rotatum':
        '''Rotatum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1480.Rotatum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Rotatum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_safety_factor(self) -> '_1481.SafetyFactor':
        '''SafetyFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1481.SafetyFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SafetyFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_specific_acoustic_impedance(self) -> '_1482.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1482.SpecificAcousticImpedance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificAcousticImpedance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_specific_heat(self) -> '_1483.SpecificHeat':
        '''SpecificHeat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1483.SpecificHeat.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificHeat. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1484.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1484.SquareRootOfUnitForcePerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_stiffness_per_unit_face_width(self) -> '_1485.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1485.StiffnessPerUnitFaceWidth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_stress(self) -> '_1486.Stress':
        '''Stress: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1486.Stress.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Stress. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature(self) -> '_1487.Temperature':
        '''Temperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1487.Temperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Temperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature_difference(self) -> '_1488.TemperatureDifference':
        '''TemperatureDifference: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1488.TemperatureDifference.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperatureDifference. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature_per_unit_time(self) -> '_1489.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1489.TemperaturePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperaturePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_text(self) -> '_1490.Text':
        '''Text: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1490.Text.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Text. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermal_contact_coefficient(self) -> '_1491.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1491.ThermalContactCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalContactCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermal_expansion_coefficient(self) -> '_1492.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1492.ThermalExpansionCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalExpansionCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermo_elastic_factor(self) -> '_1493.ThermoElasticFactor':
        '''ThermoElasticFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1493.ThermoElasticFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermoElasticFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time(self) -> '_1494.Time':
        '''Time: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1494.Time.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Time. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time_short(self) -> '_1495.TimeShort':
        '''TimeShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1495.TimeShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time_very_short(self) -> '_1496.TimeVeryShort':
        '''TimeVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1496.TimeVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque(self) -> '_1497.Torque':
        '''Torque: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1497.Torque.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Torque. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_inverse_k(self) -> '_1498.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1498.TorqueConverterInverseK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterInverseK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_k(self) -> '_1499.TorqueConverterK':
        '''TorqueConverterK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1499.TorqueConverterK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_per_unit_temperature(self) -> '_1500.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1500.TorquePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorquePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_velocity(self) -> '_1501.Velocity':
        '''Velocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1501.Velocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Velocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_velocity_small(self) -> '_1502.VelocitySmall':
        '''VelocitySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1502.VelocitySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VelocitySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_viscosity(self) -> '_1503.Viscosity':
        '''Viscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1503.Viscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Viscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_voltage(self) -> '_1504.Voltage':
        '''Voltage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1504.Voltage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Voltage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_volume(self) -> '_1505.Volume':
        '''Volume: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1505.Volume.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Volume. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_wear_coefficient(self) -> '_1506.WearCoefficient':
        '''WearCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1506.WearCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WearCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_yank(self) -> '_1507.Yank':
        '''Yank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1507.Yank.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Yank. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1393.MeasurementBase]':
        '''List[MeasurementBase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1393.MeasurementBase))
        return value


class ListWithSelectedItem_ColumnTitle(_1581.ColumnTitle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ColumnTitle

    A specific implementation of 'ListWithSelectedItem' for 'ColumnTitle' types.
    '''

    __hash__ = None
    __qualname__ = 'ColumnTitle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ColumnTitle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1581.ColumnTitle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1581.ColumnTitle.TYPE

    @property
    def selected_value(self) -> '_1581.ColumnTitle':
        '''ColumnTitle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1581.ColumnTitle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1581.ColumnTitle]':
        '''List[ColumnTitle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1581.ColumnTitle))
        return value


class ListWithSelectedItem_PowerLoad(_2208.PowerLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PowerLoad

    A specific implementation of 'ListWithSelectedItem' for 'PowerLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PowerLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2208.PowerLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2208.PowerLoad.TYPE

    @property
    def selected_value(self) -> '_2208.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2208.PowerLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2208.PowerLoad]':
        '''List[PowerLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2208.PowerLoad))
        return value


class ListWithSelectedItem_AbstractPeriodicExcitationDetail(_5658.AbstractPeriodicExcitationDetail, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_AbstractPeriodicExcitationDetail

    A specific implementation of 'ListWithSelectedItem' for 'AbstractPeriodicExcitationDetail' types.
    '''

    __hash__ = None
    __qualname__ = 'AbstractPeriodicExcitationDetail'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_AbstractPeriodicExcitationDetail.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5658.AbstractPeriodicExcitationDetail.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5658.AbstractPeriodicExcitationDetail.TYPE

    @property
    def selected_value(self) -> '_5658.AbstractPeriodicExcitationDetail':
        '''AbstractPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5658.AbstractPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_periodic_excitation_detail(self) -> '_5711.ElectricMachinePeriodicExcitationDetail':
        '''ElectricMachinePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5711.ElectricMachinePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachinePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_x_force_periodic_excitation_detail(self) -> '_5712.ElectricMachineRotorXForcePeriodicExcitationDetail':
        '''ElectricMachineRotorXForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5712.ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorXForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_x_moment_periodic_excitation_detail(self) -> '_5713.ElectricMachineRotorXMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorXMomentPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5713.ElectricMachineRotorXMomentPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorXMomentPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_y_force_periodic_excitation_detail(self) -> '_5714.ElectricMachineRotorYForcePeriodicExcitationDetail':
        '''ElectricMachineRotorYForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5714.ElectricMachineRotorYForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorYForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_y_moment_periodic_excitation_detail(self) -> '_5715.ElectricMachineRotorYMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorYMomentPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5715.ElectricMachineRotorYMomentPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorYMomentPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_z_force_periodic_excitation_detail(self) -> '_5716.ElectricMachineRotorZForcePeriodicExcitationDetail':
        '''ElectricMachineRotorZForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5716.ElectricMachineRotorZForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorZForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_axial_loads_excitation_detail(self) -> '_5717.ElectricMachineStatorToothAxialLoadsExcitationDetail':
        '''ElectricMachineStatorToothAxialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5717.ElectricMachineStatorToothAxialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothAxialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_loads_excitation_detail(self) -> '_5718.ElectricMachineStatorToothLoadsExcitationDetail':
        '''ElectricMachineStatorToothLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5718.ElectricMachineStatorToothLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_radial_loads_excitation_detail(self) -> '_5719.ElectricMachineStatorToothRadialLoadsExcitationDetail':
        '''ElectricMachineStatorToothRadialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5719.ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothRadialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_tangential_loads_excitation_detail(self) -> '_5720.ElectricMachineStatorToothTangentialLoadsExcitationDetail':
        '''ElectricMachineStatorToothTangentialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5720.ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothTangentialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_torque_ripple_periodic_excitation_detail(self) -> '_5721.ElectricMachineTorqueRipplePeriodicExcitationDetail':
        '''ElectricMachineTorqueRipplePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5721.ElectricMachineTorqueRipplePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineTorqueRipplePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_excitation_detail(self) -> '_5731.GearMeshExcitationDetail':
        '''GearMeshExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5731.GearMeshExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_misalignment_excitation_detail(self) -> '_5733.GearMeshMisalignmentExcitationDetail':
        '''GearMeshMisalignmentExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5733.GearMeshMisalignmentExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshMisalignmentExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_te_excitation_detail(self) -> '_5734.GearMeshTEExcitationDetail':
        '''GearMeshTEExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5734.GearMeshTEExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshTEExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_general_periodic_excitation_detail(self) -> '_5736.GeneralPeriodicExcitationDetail':
        '''GeneralPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5736.GeneralPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GeneralPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_periodic_excitation_with_reference_shaft(self) -> '_5765.PeriodicExcitationWithReferenceShaft':
        '''PeriodicExcitationWithReferenceShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5765.PeriodicExcitationWithReferenceShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_single_node_periodic_excitation_with_reference_shaft(self) -> '_5781.SingleNodePeriodicExcitationWithReferenceShaft':
        '''SingleNodePeriodicExcitationWithReferenceShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5781.SingleNodePeriodicExcitationWithReferenceShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SingleNodePeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_unbalanced_mass_excitation_detail(self) -> '_5806.UnbalancedMassExcitationDetail':
        '''UnbalancedMassExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5806.UnbalancedMassExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMassExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5658.AbstractPeriodicExcitationDetail]':
        '''List[AbstractPeriodicExcitationDetail]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5658.AbstractPeriodicExcitationDetail))
        return value


class ListWithSelectedItem_TupleWithName(TupleWithName, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TupleWithName

    A specific implementation of 'ListWithSelectedItem' for 'TupleWithName' types.
    '''

    __hash__ = None
    __qualname__ = 'TupleWithName'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TupleWithName.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TupleWithName.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TupleWithName.TYPE

    @property
    def selected_value(self) -> 'TupleWithName':
        '''TupleWithName: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_tuple_with_name(self.enclosing.SelectedValue, (None))
        return constructor.new(TupleWithName)(value) if value is not None else None

    @property
    def available_values(self) -> 'TupleWithName':
        '''TupleWithName: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(TupleWithName))
        return constructor.new(TupleWithName)(value) if value is not None else None


class ListWithSelectedItem_GearMeshSystemDeflection(_2489.GearMeshSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearMeshSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'GearMeshSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'GearMeshSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearMeshSystemDeflection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2489.GearMeshSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2489.GearMeshSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2489.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2489.GearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2424.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2424.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2431.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2431.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_mesh_system_deflection(self) -> '_2436.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2436.BevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_mesh_system_deflection(self) -> '_2450.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2450.ConceptGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_mesh_system_deflection(self) -> '_2454.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2454.ConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2469.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2469.CylindricalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2470.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2470.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2471.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2471.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_mesh_system_deflection(self) -> '_2484.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2484.FaceGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2493.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2493.HypoidGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2498.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2498.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2501.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2501.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2504.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2504.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2537.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2537.SpiralBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2543.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2543.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2546.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2546.StraightBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_mesh_system_deflection(self) -> '_2566.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2566.WormGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2569.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2569.ZerolBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2489.GearMeshSystemDeflection]':
        '''List[GearMeshSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2489.GearMeshSystemDeflection))
        return value


class ListWithSelectedItem_GearSet(_2267.GearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSet

    A specific implementation of 'ListWithSelectedItem' for 'GearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2267.GearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2267.GearSet.TYPE

    @property
    def selected_value(self) -> '_2267.GearSet':
        '''GearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2267.GearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set(self) -> '_2249.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.AGMAGleasonConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear_set(self) -> '_2251.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.BevelDifferentialGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_set(self) -> '_2255.BevelGearSet':
        '''BevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.BevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_set(self) -> '_2257.ConceptGearSet':
        '''ConceptGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.ConceptGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_set(self) -> '_2259.ConicalGearSet':
        '''ConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.ConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_set(self) -> '_2261.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_set(self) -> '_2264.FaceGearSet':
        '''FaceGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.FaceGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_set(self) -> '_2270.HypoidGearSet':
        '''HypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2270.HypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2272.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2272.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2274.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2274.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2276.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planetary_gear_set(self) -> '_2277.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.PlanetaryGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set(self) -> '_2279.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.SpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set(self) -> '_2281.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.StraightBevelDiffGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_set(self) -> '_2283.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.StraightBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_set(self) -> '_2287.WormGearSet':
        '''WormGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2287.WormGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set(self) -> '_2289.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.ZerolBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2267.GearSet]':
        '''List[GearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2267.GearSet))
        return value


class ListWithSelectedItem_FESubstructureNode(_2121.FESubstructureNode, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructureNode

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructureNode' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructureNode'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructureNode.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2121.FESubstructureNode.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2121.FESubstructureNode.TYPE

    @property
    def selected_value(self) -> '_2121.FESubstructureNode':
        '''FESubstructureNode: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.FESubstructureNode)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2121.FESubstructureNode]':
        '''List[FESubstructureNode]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2121.FESubstructureNode))
        return value


class ListWithSelectedItem_Datum(_2185.Datum, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Datum

    A specific implementation of 'ListWithSelectedItem' for 'Datum' types.
    '''

    __hash__ = None
    __qualname__ = 'Datum'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Datum.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2185.Datum.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2185.Datum.TYPE

    @property
    def selected_value(self) -> '_2185.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.Datum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2185.Datum]':
        '''List[Datum]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2185.Datum))
        return value


class ListWithSelectedItem_Component(_2181.Component, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Component

    A specific implementation of 'ListWithSelectedItem' for 'Component' types.
    '''

    __hash__ = None
    __qualname__ = 'Component'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Component.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2181.Component.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2181.Component.TYPE

    @property
    def selected_value(self) -> '_2181.Component':
        '''Component: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.Component.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Component. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_abstract_shaft(self) -> '_2173.AbstractShaft':
        '''AbstractShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.AbstractShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_abstract_shaft_or_housing(self) -> '_2174.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.AbstractShaftOrHousing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaftOrHousing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bearing(self) -> '_2177.Bearing':
        '''Bearing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.Bearing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bearing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bolt(self) -> '_2179.Bolt':
        '''Bolt: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.Bolt.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bolt. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_connector(self) -> '_2184.Connector':
        '''Connector: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2184.Connector.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Connector. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_datum(self) -> '_2185.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Datum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Datum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_external_cad_model(self) -> '_2188.ExternalCADModel':
        '''ExternalCADModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.ExternalCADModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ExternalCADModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fe_part(self) -> '_2189.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.FEPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FEPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_guide_dxf_model(self) -> '_2191.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.GuideDxfModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GuideDxfModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_disc(self) -> '_2198.MassDisc':
        '''MassDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.MassDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_measurement_component(self) -> '_2199.MeasurementComponent':
        '''MeasurementComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.MeasurementComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mountable_component(self) -> '_2200.MountableComponent':
        '''MountableComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.MountableComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MountableComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_oil_seal(self) -> '_2202.OilSeal':
        '''OilSeal: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2202.OilSeal.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to OilSeal. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_carrier(self) -> '_2205.PlanetCarrier':
        '''PlanetCarrier: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2205.PlanetCarrier.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrier. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_point_load(self) -> '_2207.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.PointLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_load(self) -> '_2208.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.PowerLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_unbalanced_mass(self) -> '_2213.UnbalancedMass':
        '''UnbalancedMass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.UnbalancedMass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_virtual_component(self) -> '_2215.VirtualComponent':
        '''VirtualComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.VirtualComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VirtualComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft(self) -> '_2218.Shaft':
        '''Shaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.Shaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Shaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear(self) -> '_2248.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.AGMAGleasonConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear(self) -> '_2250.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.BevelDifferentialGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_planet_gear(self) -> '_2252.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.BevelDifferentialPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_sun_gear(self) -> '_2253.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.BevelDifferentialSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear(self) -> '_2254.BevelGear':
        '''BevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.BevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear(self) -> '_2256.ConceptGear':
        '''ConceptGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.ConceptGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear(self) -> '_2258.ConicalGear':
        '''ConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.ConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear(self) -> '_2260.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planet_gear(self) -> '_2262.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.CylindricalPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear(self) -> '_2263.FaceGear':
        '''FaceGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.FaceGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear(self) -> '_2265.Gear':
        '''Gear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Gear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear(self) -> '_2269.HypoidGear':
        '''HypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2269.HypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2271.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.KlingelnbergCycloPalloidConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2273.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2275.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2275.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear(self) -> '_2278.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2278.SpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear(self) -> '_2280.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2280.StraightBevelDiffGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear(self) -> '_2282.StraightBevelGear':
        '''StraightBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.StraightBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_planet_gear(self) -> '_2284.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2284.StraightBevelPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_sun_gear(self) -> '_2285.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.StraightBevelSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear(self) -> '_2286.WormGear':
        '''WormGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.WormGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear(self) -> '_2288.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.ZerolBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cycloidal_disc(self) -> '_2304.CycloidalDisc':
        '''CycloidalDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.CycloidalDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CycloidalDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_ring_pins(self) -> '_2305.RingPins':
        '''RingPins: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.RingPins.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RingPins. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_clutch_half(self) -> '_2314.ClutchHalf':
        '''ClutchHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.ClutchHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ClutchHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_coupling_half(self) -> '_2317.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.ConceptCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_coupling_half(self) -> '_2319.CouplingHalf':
        '''CouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.CouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cvt_pulley(self) -> '_2322.CVTPulley':
        '''CVTPulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.CVTPulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CVTPulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_part_to_part_shear_coupling_half(self) -> '_2324.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2324.PartToPartShearCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PartToPartShearCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pulley(self) -> '_2325.Pulley':
        '''Pulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.Pulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rolling_ring(self) -> '_2331.RollingRing':
        '''RollingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2331.RollingRing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft_hub_connection(self) -> '_2333.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.ShaftHubConnection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spring_damper_half(self) -> '_2336.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2336.SpringDamperHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpringDamperHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_half(self) -> '_2339.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.SynchroniserHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_part(self) -> '_2340.SynchroniserPart':
        '''SynchroniserPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2340.SynchroniserPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_sleeve(self) -> '_2341.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.SynchroniserSleeve.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserSleeve. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_pump(self) -> '_2343.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2343.TorqueConverterPump.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterPump. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_turbine(self) -> '_2345.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2345.TorqueConverterTurbine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterTurbine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2181.Component]':
        '''List[Component]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2181.Component))
        return value


class ListWithSelectedItem_FELink(_2154.FELink, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FELink

    A specific implementation of 'ListWithSelectedItem' for 'FELink' types.
    '''

    __hash__ = None
    __qualname__ = 'FELink'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FELink.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2154.FELink.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2154.FELink.TYPE

    @property
    def selected_value(self) -> '_2154.FELink':
        '''FELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.FELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_fe_link(self) -> '_2155.ElectricMachineStatorFELink':
        '''ElectricMachineStatorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.ElectricMachineStatorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_fe_link(self) -> '_2157.GearMeshFELink':
        '''GearMeshFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.GearMeshFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_with_duplicated_meshes_fe_link(self) -> '_2158.GearWithDuplicatedMeshesFELink':
        '''GearWithDuplicatedMeshesFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.GearWithDuplicatedMeshesFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearWithDuplicatedMeshesFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_angle_connection_fe_link(self) -> '_2159.MultiAngleConnectionFELink':
        '''MultiAngleConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.MultiAngleConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiAngleConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_node_connector_fe_link(self) -> '_2160.MultiNodeConnectorFELink':
        '''MultiNodeConnectorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.MultiNodeConnectorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeConnectorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_node_fe_link(self) -> '_2161.MultiNodeFELink':
        '''MultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.MultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planetary_connector_multi_node_fe_link(self) -> '_2162.PlanetaryConnectorMultiNodeFELink':
        '''PlanetaryConnectorMultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.PlanetaryConnectorMultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryConnectorMultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_based_fe_link(self) -> '_2163.PlanetBasedFELink':
        '''PlanetBasedFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.PlanetBasedFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetBasedFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_carrier_fe_link(self) -> '_2164.PlanetCarrierFELink':
        '''PlanetCarrierFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2164.PlanetCarrierFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrierFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_point_load_fe_link(self) -> '_2165.PointLoadFELink':
        '''PointLoadFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2165.PointLoadFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoadFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rolling_ring_connection_fe_link(self) -> '_2166.RollingRingConnectionFELink':
        '''RollingRingConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2166.RollingRingConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRingConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft_hub_connection_fe_link(self) -> '_2167.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2167.ShaftHubConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_single_node_fe_link(self) -> '_2168.SingleNodeFELink':
        '''SingleNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2168.SingleNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SingleNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2154.FELink]':
        '''List[FELink]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2154.FELink))
        return value


class ListWithSelectedItem_FESubstructure(_2119.FESubstructure, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructure

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructure' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructure'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructure.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2119.FESubstructure.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2119.FESubstructure.TYPE

    @property
    def selected_value(self) -> '_2119.FESubstructure':
        '''FESubstructure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.FESubstructure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2119.FESubstructure]':
        '''List[FESubstructure]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2119.FESubstructure))
        return value


class ListWithSelectedItem_CylindricalGear(_2260.CylindricalGear, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGear

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGear' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGear'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGear.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2260.CylindricalGear.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2260.CylindricalGear.TYPE

    @property
    def selected_value(self) -> '_2260.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2260.CylindricalGear]':
        '''List[CylindricalGear]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2260.CylindricalGear))
        return value


class ListWithSelectedItem_GuideDxfModel(_2191.GuideDxfModel, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GuideDxfModel

    A specific implementation of 'ListWithSelectedItem' for 'GuideDxfModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GuideDxfModel'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GuideDxfModel.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2191.GuideDxfModel.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2191.GuideDxfModel.TYPE

    @property
    def selected_value(self) -> '_2191.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.GuideDxfModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2191.GuideDxfModel]':
        '''List[GuideDxfModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2191.GuideDxfModel))
        return value


class ListWithSelectedItem_ConcentricPartGroup(_2223.ConcentricPartGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConcentricPartGroup

    A specific implementation of 'ListWithSelectedItem' for 'ConcentricPartGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ConcentricPartGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConcentricPartGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2223.ConcentricPartGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2223.ConcentricPartGroup.TYPE

    @property
    def selected_value(self) -> '_2223.ConcentricPartGroup':
        '''ConcentricPartGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.ConcentricPartGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2223.ConcentricPartGroup]':
        '''List[ConcentricPartGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2223.ConcentricPartGroup))
        return value


class ListWithSelectedItem_CylindricalGearSet(_2261.CylindricalGearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSet

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2261.CylindricalGearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2261.CylindricalGearSet.TYPE

    @property
    def selected_value(self) -> '_2261.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2261.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2261.CylindricalGearSet))
        return value


class ListWithSelectedItem_GearSetDesign(_902.GearSetDesign, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSetDesign

    A specific implementation of 'ListWithSelectedItem' for 'GearSetDesign' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSetDesign'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSetDesign.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_902.GearSetDesign.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _902.GearSetDesign.TYPE

    @property
    def selected_value(self) -> '_902.GearSetDesign':
        '''GearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _902.GearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set_design(self) -> '_906.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _906.ZerolBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_set_design(self) -> '_911.WormGearSetDesign':
        '''WormGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.WormGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set_design(self) -> '_915.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.StraightBevelDiffGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_set_design(self) -> '_919.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.StraightBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set_design(self) -> '_923.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _923.SpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_927.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _927.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_931.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _931.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_conical_gear_set_design(self) -> '_935.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _935.KlingelnbergConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_set_design(self) -> '_939.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _939.HypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_set_design(self) -> '_947.FaceGearSetDesign':
        '''FaceGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _947.FaceGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_set_design(self) -> '_979.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _979.CylindricalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planetary_gear_set_design(self) -> '_990.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _990.CylindricalPlanetaryGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_set_design(self) -> '_1098.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1098.ConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_set_design(self) -> '_1120.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1120.ConceptGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_set_design(self) -> '_1124.BevelGearSetDesign':
        '''BevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1124.BevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set_design(self) -> '_1137.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1137.AGMAGleasonConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_902.GearSetDesign]':
        '''List[GearSetDesign]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_902.GearSetDesign))
        return value


class ListWithSelectedItem_ShaftHubConnection(_2333.ShaftHubConnection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ShaftHubConnection

    A specific implementation of 'ListWithSelectedItem' for 'ShaftHubConnection' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftHubConnection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ShaftHubConnection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2333.ShaftHubConnection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2333.ShaftHubConnection.TYPE

    @property
    def selected_value(self) -> '_2333.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2333.ShaftHubConnection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2333.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2333.ShaftHubConnection))
        return value


class ListWithSelectedItem_TSelectableItem(Generic[TSelectableItem], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TSelectableItem

    A specific implementation of 'ListWithSelectedItem' for 'TSelectableItem' types.
    '''

    __hash__ = None
    __qualname__ = 'TSelectableItem'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TSelectableItem.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TSelectableItem':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TSelectableItem

    @property
    def selected_value(self) -> 'TSelectableItem':
        '''TSelectableItem: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[TSelectableItem]':
        '''List[TSelectableItem]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_CylindricalGearSystemDeflection(_2475.CylindricalGearSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSystemDeflection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2475.CylindricalGearSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2475.CylindricalGearSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2475.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2475.CylindricalGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2476.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2476.CylindricalGearSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2477.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2477.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2480.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2480.CylindricalPlanetGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2475.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2475.CylindricalGearSystemDeflection))
        return value


class ListWithSelectedItem_DesignState(_5383.DesignState, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DesignState

    A specific implementation of 'ListWithSelectedItem' for 'DesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignState'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DesignState.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5383.DesignState.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5383.DesignState.TYPE

    @property
    def selected_value(self) -> '_5383.DesignState':
        '''DesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5383.DesignState)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5383.DesignState]':
        '''List[DesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5383.DesignState))
        return value


class ListWithSelectedItem_FEPart(_2189.FEPart, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FEPart

    A specific implementation of 'ListWithSelectedItem' for 'FEPart' types.
    '''

    __hash__ = None
    __qualname__ = 'FEPart'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FEPart.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2189.FEPart.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2189.FEPart.TYPE

    @property
    def selected_value(self) -> '_2189.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.FEPart)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2189.FEPart]':
        '''List[FEPart]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2189.FEPart))
        return value


class ListWithSelectedItem_TPartAnalysis(Generic[TPartAnalysis], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TPartAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'TPartAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'TPartAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TPartAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TPartAnalysis':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TPartAnalysis

    @property
    def selected_value(self) -> 'TPartAnalysis':
        '''TPartAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[TPartAnalysis]':
        '''List[TPartAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ResultLocationSelectionGroup(_5822.ResultLocationSelectionGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ResultLocationSelectionGroup

    A specific implementation of 'ListWithSelectedItem' for 'ResultLocationSelectionGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ResultLocationSelectionGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ResultLocationSelectionGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5822.ResultLocationSelectionGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5822.ResultLocationSelectionGroup.TYPE

    @property
    def selected_value(self) -> '_5822.ResultLocationSelectionGroup':
        '''ResultLocationSelectionGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5822.ResultLocationSelectionGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5822.ResultLocationSelectionGroup]':
        '''List[ResultLocationSelectionGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5822.ResultLocationSelectionGroup))
        return value


class ListWithSelectedItem_StaticLoadCase(_6514.StaticLoadCase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_StaticLoadCase

    A specific implementation of 'ListWithSelectedItem' for 'StaticLoadCase' types.
    '''

    __hash__ = None
    __qualname__ = 'StaticLoadCase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_StaticLoadCase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_6514.StaticLoadCase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6514.StaticLoadCase.TYPE

    @property
    def selected_value(self) -> '_6514.StaticLoadCase':
        '''StaticLoadCase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6514.StaticLoadCase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StaticLoadCase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_6514.StaticLoadCase]':
        '''List[StaticLoadCase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_6514.StaticLoadCase))
        return value


class ListWithSelectedItem_DutyCycle(_5384.DutyCycle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DutyCycle

    A specific implementation of 'ListWithSelectedItem' for 'DutyCycle' types.
    '''

    __hash__ = None
    __qualname__ = 'DutyCycle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DutyCycle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5384.DutyCycle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5384.DutyCycle.TYPE

    @property
    def selected_value(self) -> '_5384.DutyCycle':
        '''DutyCycle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5384.DutyCycle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5384.DutyCycle]':
        '''List[DutyCycle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5384.DutyCycle))
        return value


class ListWithSelectedItem_float(float, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_float

    A specific implementation of 'ListWithSelectedItem' for 'float' types.
    '''

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else 0.0)

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def selected_value(self) -> 'float':
        '''float: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[float]':
        '''List[float]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ElectricMachineDataSet(_2110.ElectricMachineDataSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ElectricMachineDataSet

    A specific implementation of 'ListWithSelectedItem' for 'ElectricMachineDataSet' types.
    '''

    __hash__ = None
    __qualname__ = 'ElectricMachineDataSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ElectricMachineDataSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2110.ElectricMachineDataSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2110.ElectricMachineDataSet.TYPE

    @property
    def selected_value(self) -> '_2110.ElectricMachineDataSet':
        '''ElectricMachineDataSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.ElectricMachineDataSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2110.ElectricMachineDataSet]':
        '''List[ElectricMachineDataSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2110.ElectricMachineDataSet))
        return value


class ListWithSelectedItem_PointLoad(_2207.PointLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PointLoad

    A specific implementation of 'ListWithSelectedItem' for 'PointLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PointLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2207.PointLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2207.PointLoad.TYPE

    @property
    def selected_value(self) -> '_2207.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2207.PointLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2207.PointLoad]':
        '''List[PointLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2207.PointLoad))
        return value
