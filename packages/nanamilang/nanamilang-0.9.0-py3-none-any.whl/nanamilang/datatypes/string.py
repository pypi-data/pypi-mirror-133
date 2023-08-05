"""NanamiLang String Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class String(Base):
    """NanamiLang String Data Type Class"""

    name: str = 'String'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    def format(self, **_) -> str:
        """NanamiLang String, format() method implementation"""

        return f'"{self.reference()}"'

    def truthy(self) -> bool:
        """NanamiLang String, truthy() method implementation"""

        return True
        # In Python 3 by default, all empty strings are not truthy, but not in Clojure
