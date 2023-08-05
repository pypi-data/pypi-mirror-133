"""NanamiLang Module Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import time
from typing import List, Dict

from nanamilang.ast import AST
from nanamilang.formatter import Formatter
from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from nanamilang.shortcuts import ASSERT_IS_INSTANCE_OF
from nanamilang.token import Token
from nanamilang.tokenizer import Tokenizer


class Module:
    """
    NanamiLang Module

    from nanamilang import module

    source = str('(+ 2 2 (* 2 2))')
    m = module.Module(source=source)

    # or

    m: module.Module = module.Module()
    m.prepare(source)

    m.format() # => '(+ 2 2 (* 2 2))'
    m.ast() # => get encapsulated AST instance
    m.tokenized() # => collection of a Token instances

    results = m.evaluate() # => ((<IntegerNumber>: 8, ...),)
    """

    _ast: AST
    _name: str
    _source: str
    _globals: dict = None
    _formatter = Formatter
    _tokenized: List[Token]
    _evaluation_results = tuple
    _measurements: Dict[str, float] = {}

    def __init__(self,
                 name: str = None,
                 source: str = None) -> None:
        """
        Initialize a new NanamiLang Module instance

        :param source: your NanamiLang module source code
        """

        self._globals = {}
        self._name = name or '__main__'

        # Module name is optional value, but if present - set to it

        if source:
            self.prepare(source)

        # Source code is optional value, but if present - call prepare

    def name(self):
        """NanamiLang Module, self._name getter"""

        return self._name

    def globals(self):
        """NanamiLang Module, self._globals getter"""

        return self._globals

    def prepare(self, source: str):
        """NanamiLang Module, prepare a source code"""

        ASSERT_IS_INSTANCE_OF(source, str)
        ASSERT_COLLECTION_IS_NOT_EMPTY(source)

        self._source = source
        __tokenize_start__ = time.perf_counter()
        self._tokenized = Tokenizer(source=self._source,
                                    name=self._name).tokenize()
        __tokenize_delta__ = time.perf_counter() - __tokenize_start__
        __make_wood_start__ = time.perf_counter()
        self._ast = AST(self._tokenized)
        __make_wood_delta__ = time.perf_counter() - __make_wood_start__
        self._formatter = Formatter(self._tokenized)
        self._measurements = {
            '[Tree]': __make_wood_delta__, '[Parse]': __tokenize_delta__,
        }

    def ast(self) -> AST:
        """NanamiLang Module, self._ast getter"""

        return self._ast

    def tokenized(self) -> List[Token]:
        """NanamiLang Module, self._tokenized getter"""

        return self._tokenized

    def measurements(self) -> Dict[str, float]:
        """NanamiLang Module, self._measurements getter"""

        return self._measurements

    def results(self) -> tuple:
        """NanamiLang Module, self.__evaluation_results getter"""

        return self._evaluation_results

    def format(self) -> str:
        """NanamiLang Module, call self._formatter.format() to format source"""

        return self._formatter.format()

    def evaluate(self) -> 'Module':
        """NanamiLang Module, call self._ast.evaluate() to evaluate your module"""

        __evaluate_start__ = time.perf_counter()
        self._evaluation_results = self._ast.evaluate(self._globals)
        __evaluate_delta__ = time.perf_counter() - __evaluate_start__
        self._measurements.update({'[Evaluation]': __evaluate_delta__})
        return self

        # Measure [Evaluation] time and store measurement in self._measurements dictionary
        # Return all evaluated trees of the self.ast().wood() to a Module.evaluate() caller
