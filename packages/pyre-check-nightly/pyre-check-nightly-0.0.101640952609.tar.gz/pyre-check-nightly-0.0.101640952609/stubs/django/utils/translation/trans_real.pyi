# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe

import gettext as gettext_module
from typing import Any

def translation(language: Any) -> DjangoTranslation: ...

class DjangoTranslation(gettext_module.GNUTranslations):
    def __init__(self, language): ...
    def _new_gnu_trans(self, localedir, use_null_fallback=True): ...
    def _init_translation_catalog(self): ...
    def _add_installed_apps_translations(self): ...
    def _add_local_translations(self): ...
    def _add_fallback(self): ...
    def merge(self, other): ...
    def language(self): ...
    def to_language(self): ...
