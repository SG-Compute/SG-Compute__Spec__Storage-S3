# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute — Schema__Spec__Catalogue
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                   import List

from osbot_utils.type_safe.Type_Safe                                          import Type_Safe


class Schema__Spec__Catalogue(Type_Safe):
    specs : List = None

    def __init__(self, specs=None):
        self.specs = specs or []
