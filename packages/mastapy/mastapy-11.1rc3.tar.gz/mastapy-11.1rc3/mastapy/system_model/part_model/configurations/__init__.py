'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2346 import ActiveFESubstructureSelection
    from ._2347 import ActiveFESubstructureSelectionGroup
    from ._2348 import ActiveShaftDesignSelection
    from ._2349 import ActiveShaftDesignSelectionGroup
    from ._2350 import BearingDetailConfiguration
    from ._2351 import BearingDetailSelection
    from ._2352 import PartDetailConfiguration
    from ._2353 import PartDetailSelection
