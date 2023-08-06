'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2079 import ClutchConnection
    from ._2080 import ClutchSocket
    from ._2081 import ConceptCouplingConnection
    from ._2082 import ConceptCouplingSocket
    from ._2083 import CouplingConnection
    from ._2084 import CouplingSocket
    from ._2085 import PartToPartShearCouplingConnection
    from ._2086 import PartToPartShearCouplingSocket
    from ._2087 import SpringDamperConnection
    from ._2088 import SpringDamperSocket
    from ._2089 import TorqueConverterConnection
    from ._2090 import TorqueConverterPumpSocket
    from ._2091 import TorqueConverterTurbineSocket
