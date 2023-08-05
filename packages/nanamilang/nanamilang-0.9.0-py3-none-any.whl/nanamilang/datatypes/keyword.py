"""NanamiLang Keyword Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Keyword(Base):
    """NanamiLang Keyword Data Type Class"""

    name: str = 'Keyword'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    def format(self, **_) -> str:
        """NanamiLang Keyword, format() method implementation"""

        return f':{self._python_reference}'

    def _additional_assertions_on_init(self, reference) -> None:
        """NanamiLang Keyword, _additional_assertions_on_init() method implementation"""

        self._init_assert_ref_could_not_be_empty(reference)
        # Since Keyword encapsulates a Python 3 str, be sure that that string is not empty
