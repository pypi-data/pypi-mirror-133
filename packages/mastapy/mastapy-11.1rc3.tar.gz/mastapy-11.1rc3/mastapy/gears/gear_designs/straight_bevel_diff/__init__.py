﻿'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._913 import StraightBevelDiffGearDesign
    from ._914 import StraightBevelDiffGearMeshDesign
    from ._915 import StraightBevelDiffGearSetDesign
    from ._916 import StraightBevelDiffMeshedGearDesign
