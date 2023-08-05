"""NanamiLang Program Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


class Program:
    """
    NanamiLang Program

    from nanamilang import program, module

    source = str('(+ 2 2 (* 2 2))')
    m = module.Module(source=source)
    m.format() # => '(+ 2 2 (* 2 2))'
    m.ast() # => get encapsulated AST instance
    m.tokenized() # => collection of a Token instances

    p = program.Program([m])

    results = p.evaluate() # => tuple of (re)evaluated modules
    """

    _module_list: list = []

    def __init__(self, modules: list) -> None:
        """
        Initialize a new NanamiLang Program instance

        :param modules: your NanamiLang program modules
        """

        if modules:
            self._module_list = modules
        else:
            raise AssertionError('program: at least one module is required to process')

    def modules(self) -> list:
        """NanamiLang Program, call self._modules getter"""

        return self._module_list

    def evaluate(self) -> dict:
        """NanamiLang Program, call evaluate() on each program module, return modules"""

        return {module.name(): module.evaluate() for module in self.modules()}

        # Return a dict {name: instance} of evaluated program modules to a 'Program.evaluate()' caller
