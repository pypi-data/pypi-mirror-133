"""NanamiLang BuiltinMacros and BuiltinFunctions classes"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import functools
from functools import reduce
from typing import List

from nanamilang import fn, datatypes, loader
from nanamilang.shortcuts import get
from nanamilang.shortcuts import (
    NML_M_ASSERT_FORM_IS_A_VALID_HASHMAP,
    NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS,
    NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS_EVEN,
    NML_M_ASSERT_FORM_IS_A_HASHMAP, NML_M_ITERATE_AS_PAIRS,
    NML_M_ASSERT_FORM_IS_A_VECTOR, ASSERT_DICT_CONTAINS_KEY
)
from nanamilang.shortcuts import randstr, plain2partitioned
from nanamilang.spec import Spec


def meta(data: dict):
    """
    NanamiLang, apply meta data to a function
    'name': fn or macro LISP name
    'type': 'macro' or 'function'
    'forms': possible fn or macro possible forms
    'docstring': what fn or macro actually does?
    May contain 'hidden' (do not show in completions)
    May contain 'spec' attribute, but its not required

    :param data: a function meta data Python dictionary
    """

    def wrapped(_fn):
        @functools.wraps(_fn)
        def function(*args, **kwargs):
            spec = data.get('spec')
            if spec:
                if data.get('type') == 'macro':
                    Spec.validate(data.get('name'), args[1], spec)
                else:
                    Spec.validate(data.get('name'), args[0], spec)

            return _fn(*args, **kwargs)

        # TODO: maybe also implement spec linting

        ASSERT_DICT_CONTAINS_KEY('name', data, 'function meta data must contain a name')
        ASSERT_DICT_CONTAINS_KEY('type', data, 'function meta data must contain a type')
        ASSERT_DICT_CONTAINS_KEY('forms', data, 'function meta data must contain a forms')
        ASSERT_DICT_CONTAINS_KEY('docstring', data, 'function meta data must contain a docstring')

        function.meta = data

        return function

    return wrapped


class BuiltinMacros:
    """NanamiLang Builtin Macros"""

    cached = {}

    #################################################################################################################

    @staticmethod
    def resolve(mc_name: str) -> dict:
        """Resolve macro by its name"""

        if fun := BuiltinMacros.cached.get(mc_name, {}):
            return fun
        for macro in BuiltinMacros.functions():
            if macro.meta.get('name') == mc_name:
                resolved: dict = {'macro_name': mc_name,
                                  'macro_reference': macro}
                BuiltinMacros.cached.update({mc_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinMacros.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _macro functions"""

        attrib_names = filter(lambda _: '_macro' in _, BuiltinMacros().__dir__())

        return list(map(lambda n: getattr(BuiltinMacros, n, None), attrib_names))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->',
           'type': 'macro',
           'forms': ['(-> form1 form2 ... formN)'],
           'docstring': 'Allows to write code as a pipeline'})
    def first_threading_macro(token_cls,
                              tree: list,
                              *_: tuple) -> list:
        """
        Builtin '->' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param _: unused argument, but i need to mention it here
        :return: modified or new source tree as it would be expected
        """

        if len(tree) > 1:

            for idx, tof in enumerate(tree):
                if len(tree) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier,
                                         'identity'),
                               tof]
                    next_tof = tree[idx + 1]
                    if not isinstance(next_tof, list):
                        tree[idx + 1] = [next_tof, tof]
                    else:
                        tree[idx + 1].insert(1, tof)

            return tree[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree[-1]]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->>',
           'type': 'macro',
           'forms': ['(->> form1 form2 ... formN)'],
           'docstring': 'Allows to write code as a pipeline'})
    def last_threading_macro(token_cls,
                             tree: list,
                             *_: tuple) -> list:
        """
        Builtin '->>' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param _: unused argument, but i need to mention it here
        :return: modified or new source tree as it would be expected
        """

        if len(tree) > 1:

            for idx, tof in enumerate(tree):
                if len(tree) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier,
                                         'identity'),
                               tof]
                    next_tof = tree[idx + 1]
                    if not isinstance(next_tof, list):
                        tree[idx + 1] = [next_tof, tof]
                    else:
                        tree[idx + 1].append(tof)

            return tree[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree[-1]]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 3]],
           'name': 'if',
           'type': 'macro',
           'forms': ['(if cond true-branch else-branch)'],
           'docstring': 'Returns true/else depending on cond'})
    def if_macro(token_cls,
                 tree: list,
                 local_env: dict,
                 _,
                 eval_function) -> list:
        """
        Builtin 'if' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        cond, true_branch, else_branch = tree

        if not isinstance(cond, list):
            cond = [token_cls(
                token_cls.Identifier, 'identity'), cond]
        if not isinstance(true_branch, list):
            true_branch = [token_cls(
                token_cls.Identifier, 'identity'), true_branch]
        if not isinstance(else_branch, list):
            else_branch = [token_cls(
                token_cls.Identifier, 'identity'), else_branch]

        evaluated = eval_function(local_env, cond)
        if isinstance(evaluated, datatypes.NException):
            return [token_cls(token_cls.Identifier, 'identity'),
                    token_cls(token_cls.Proxy, evaluated)]

        return true_branch if evaluated.truthy() is True else else_branch

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'cond',
           'type': 'macro',
           'forms': ['(cond cond1 expr1 ... condN exprN)'],
           'docstring': 'Allows you to describe your cond-expr pairs'})
    def cond_macro(token_cls,
                   tree: list,
                   local_env: dict,
                   _,
                   eval_function) -> list:
        """
        Builtin 'cond' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        for [cond, expr] in plain2partitioned(tree):
            if not isinstance(cond, list):
                cond = [token_cls(token_cls.Identifier, 'identity'), cond]

            evaluated = eval_function(local_env, cond)
            if isinstance(evaluated, datatypes.NException):
                return [token_cls(token_cls.Identifier, 'identity'),
                        token_cls(token_cls.Proxy, evaluated)]

            if evaluated.truthy():
                return expr \
                    if isinstance(expr, list) \
                    else [token_cls(token_cls.Identifier, 'identity'), expr]
        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'comment',
           'type': 'macro',
           'forms': ['(comment ...)'],
           'docstring': 'Allows you to replace entire form with a Nil'})
    def comment_macro(token_cls,
                      *_: tuple) -> list:
        """
        Builtin 'comment' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param _: unused argument, but i need to mention it here
        :return: modified or new source tree as it would be expected
        """

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [2, 3]]],
           'name': 'fn',
           'type': 'macro',
           'forms': ['(fn [p1 p2 ...] body)',
                     '(fn name [p1 p2 ...] body)'],
           'docstring': 'Allows to define anonymous function, maybe named'})
    def fn_macro(token_cls,
                 tree: list,
                 local_env: dict,
                 _,
                 eval_function) -> list:
        """
        Builtin 'fn' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        name_token, parameters_form, body_token_or_form = [None] * 3

        if len(tree) == 2:
            parameters_form, body_token_or_form = tree
        elif len(tree) == 3:
            name_token, parameters_form, body_token_or_form = tree
            assert not isinstance(name_token, list), 'fn: name needs to be a token, not a form'
            assert name_token.type() == token_cls.Identifier, 'fn: name needs to be Identifier'

        NML_M_ASSERT_FORM_IS_A_VECTOR(parameters_form, 'fn: parameters form needs to be a Vector')

        parameters = []
        for parameter_tof in NML_M_ITERATE_AS_PAIRS(parameters_form):
            if isinstance(parameter_tof, list):
                assert parameter_tof[0].dt().origin() == 'make-vector',  'fn: needs to be Vector'
                right = []
                for x in NML_M_ITERATE_AS_PAIRS(parameter_tof):
                    assert x.type() == token_cls.Identifier, 'fn: is not an Identifier'
                    right.append(x.dt().origin())
                parameters.append((f'{randstr()}', right))
            else:
                assert parameter_tof.type() == token_cls.Identifier,   'fn: is not an Identifier'
                parameters.append((parameter_tof.dt().origin(), None))

        name = name_token.dt().origin() if name_token else randstr()

        fni = fn.Fn(token_cls, body_token_or_form, local_env, eval_function, name, parameters)
        handle = lambda args: fni.handle(tuple(args))

        handle.meta = {
            'name': name, 'docstring': '',
            'type': 'function', 'forms': fni.generate_meta__forms()
        }

        payload = {name: datatypes.Function({'function_name': name,
                                             'function_reference': handle})}

        local_env.update(payload)
        fni.env().update(payload)

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Identifier, name)]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'and',
           'type': 'macro',
           'forms': ['(and cond1 cond2 ... condN)'],
           'docstring': 'Returns true if empty form, compares truths'})
    def and_macro(token_cls,
                  tree: list,
                  local_env: dict,
                  _,
                  eval_function) -> list:
        """
        Builtin 'and' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        if not tree:
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Boolean, True)]

        for condition in tree:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]

            evaluated = eval_function(local_env, condition)
            if isinstance(evaluated, datatypes.NException):
                return [token_cls(token_cls.Identifier, 'identity'),
                        token_cls(token_cls.Proxy, evaluated)]

            if not evaluated.truthy():
                return condition

        last = tree[-1]
        return last if isinstance(last, list) else [token_cls(token_cls.Identifier, 'identity'), last]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'or',
           'type': 'macro',
           'forms': ['(or cond1 cond2 ... condN)'],
           'docstring': 'Returns a nil if empty form, compares truths'})
    def or_macro(token_cls,
                 tree: list,
                 local_env: dict,
                 _,
                 eval_function) -> list:
        """
        Builtin 'or' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        if not tree:
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

        for condition in tree:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]

            evaluated = eval_function(local_env, condition)
            if isinstance(evaluated, datatypes.NException):
                return [token_cls(token_cls.Identifier, 'identity'),
                        token_cls(token_cls.Proxy, evaluated)]

            if evaluated.truthy():
                return condition

        last = tree[-1]
        return last if isinstance(last, list) else [token_cls(token_cls.Identifier, 'identity'), last]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'def',
           'type': 'macro',
           'forms': ['(def binding value)'],
           'docstring': 'Allows to define global binding and access it later'})
    def def_macro(token_cls,
                  tree: list,
                  local_env: dict,
                  module_env,
                  eval_function) -> list:
        """
        Builtin 'def' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param module_env: module environment we are free to modify
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        binding_token, value_token_or_form = tree

        assert not isinstance(binding_token, list), 'def: binding could not be a form'
        assert binding_token.type() == token_cls.Identifier, 'def: binding needs to be an Identifier'

        value_token_or_form = value_token_or_form \
            if isinstance(value_token_or_form, list)\
            else [token_cls(token_cls.Identifier, 'identity'), value_token_or_form]

        evaluated = eval_function(local_env, value_token_or_form)
        if isinstance(evaluated, datatypes.NException):
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Proxy, evaluated)]

        binding_name = binding_token.dt().origin()

        module_env.set(binding_name, evaluated)

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Identifier, binding_name)]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [3, 4, 5]]],
           'name': 'defn',
           'type': 'macro',
           'forms': ['(defn name [p1 p2 ...] body)',
                     '(defn name docstring [p1 p2 ...] body)',
                     '(defn name docstring spec [p1 p2 ...] body)'],
           'docstring': 'Allows to define named (maybe documented) function'})
    def defn_macro(token_cls,
                   tree: list,
                   local_env: dict,
                   module_env,
                   eval_function) -> list:
        """
        Builtin 'defn' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param module_env: module environment we are free to modify
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        name_token, docstring_token, spec_form, parameters_form, body_token_or_form = [None] * 5

        if len(tree) == 3:
            name_token, parameters_form, body_token_or_form = tree
        elif len(tree) == 4:
            name_token, docstring_token, parameters_form, body_token_or_form = tree
        elif len(tree) == 5:
            name_token, docstring_token, spec_form, parameters_form, body_token_or_form = tree

        assert not isinstance(name_token, list), 'defn: name needs to be a token, not a form'
        assert name_token.type() == token_cls.Identifier, 'defn: name needs to be Identifier'

        if docstring_token:
            assert not isinstance(docstring_token, list), 'defn: docstring needs to be a token, not a form'
            assert docstring_token.type() == token_cls.String, 'defn: docstring needs to be a String'

        ####################################################################################################

        # TODO: support more spec values

        spec_list = None  # <- even if there is no spec form has passed, I need to define local variable :))

        if spec_form:
            NML_M_ASSERT_FORM_IS_A_HASHMAP(spec_form, 'defn: spec form needs to be a Hashmap')
            NML_M_ASSERT_FORM_IS_A_VALID_HASHMAP(spec_form, 'defn: spec form needs to be a _valid_ HashMap')

            spec_list = []

            for nml_hs_k, nml_hs_v in NML_M_ITERATE_AS_PAIRS(spec_form, 2):
                if nml_hs_k.type() == token_cls.Keyword and nml_hs_k.dt().reference() == 'nanamilang-spec':
                    for nml_vc_e in NML_M_ITERATE_AS_PAIRS(nml_hs_v):
                        for nml_kw, nml_simple in NML_M_ITERATE_AS_PAIRS(nml_vc_e, 2):
                            spec_list.append([
                                {'arity-is': Spec.ArityIs,
                                 'arity-even': Spec.ArityEven,
                                 'arity-variants': Spec.ArityVariants,
                                 'arity-at-least-one': Spec.ArityAtLeastOne,
                                 'each-argument-type-is': Spec.EachArgumentTypeIs,
                                 'each-argument-type-variants': Spec.EachArgumentTypeVariants,
                                 'arguments-type-chain-variants': Spec.ArgumentsTypeChainVariants}.get(
                                    nml_kw.dt().reference()
                                ), datatypes.DataType.resolve(nml_simple.dt().reference())
                                if nml_simple.type() == token_cls.String else nml_simple.reference()])  # :/

        ####################################################################################################

        NML_M_ASSERT_FORM_IS_A_VECTOR(parameters_form, 'defn: parameters form needs to be a Vector')

        parameters = []
        for parameter_tof in NML_M_ITERATE_AS_PAIRS(parameters_form):
            if isinstance(parameter_tof, list):
                assert parameter_tof[0].dt().origin() == 'make-vector',  'defn: needs to be Vector'
                right = []
                for x in NML_M_ITERATE_AS_PAIRS(parameter_tof):
                    assert x.type() == token_cls.Identifier, 'defn: is not an Identifier'
                    right.append(x.dt().origin())
                parameters.append((f'{randstr()}', right))
            else:
                assert parameter_tof.type() == token_cls.Identifier,   'defn: is not an Identifier'
                parameters.append((parameter_tof.dt().origin(), None))

        function_name = name_token.dt().origin()

        fni = fn.Fn(token_cls,
                    body_token_or_form,
                    local_env,
                    eval_function, function_name, parameters, optionally_nanamilang_spec=spec_list)
        handle = lambda args: fni.handle(tuple(args))

        handle.meta = {
            'name': function_name, 'docstring': docstring_token.dt().reference() if docstring_token else '',
            'type': 'function', 'forms': fni.generate_meta__forms()
        }

        module_env.set(function_name, datatypes.Function({'function_name': function_name,
                                                          'function_reference': handle}))

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Identifier, function_name)]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'require',
           'type': 'macro',
           'forms': ['(require \'module-name)'],
           'docstring': 'Allows to require *.nml module'})
    def require_macro(token_cls,
                      tree: list,
                      _,
                      module_env,
                      __) -> list:
        """
        Builtin 'require' macro implementation
        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param _: unused argument, but i need to mention it here
        :param module_env: module environment we are free to modify
        :param __: also an unused argument i need to mention it here
        :return: modified or new source tree as it would be expected
        """

        # We make it a macro because functions has no access to global environment

        # This is pretty dumb implementation of (require 'module) functionality, shame on me >_<

        module_name_token = tree[0]
        assert module_name_token.type() == token_cls.Symbol, 'require: module name needs to be Symbol'

        loader.Loader.load(module_name_token.dt().reference(), module_env)  # <- should take care of module_env

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]  # like in Clojure

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'for',
           'type': 'macro',
           'forms': ['(for [identifier coll] using-token-or-form)'],
           'docstring': 'Iterates through an evaluated collection'})
    def for_macro(token_cls,
                  tree: list,
                  local_env: dict,
                  _,
                  eval_function) -> list:
        """
        Builtin 'for' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        identifier_coll_vector_form, using_token_or_form = tree

        NML_M_ASSERT_FORM_IS_A_VECTOR(identifier_coll_vector_form, 'for: first argument needs to be a Vector')

        NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS(identifier_coll_vector_form, 2,
                                              'for: first arguments should contain identifier and collection')

        identifier_token, coll_token_or_form = tuple(NML_M_ITERATE_AS_PAIRS(identifier_coll_vector_form))

        coll_token_or_form = coll_token_or_form if isinstance(coll_token_or_form, list) else (
            [token_cls(token_cls.Identifier, 'identity'), coll_token_or_form]
        )

        assert identifier_token.type() == token_cls.Identifier, 'for: an identifier needs to be an Identifier'

        evaluated_coll_or_nexc = eval_function(local_env, coll_token_or_form)
        if isinstance(evaluated_coll_or_nexc, datatypes.NException):
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Proxy, evaluated_coll_or_nexc)]

        assert isinstance(evaluated_coll_or_nexc, datatypes.Vector), 'for: evaluated collection needs to be a Vector'

        using_token_or_form = using_token_or_form if isinstance(using_token_or_form, list) else (
            [token_cls(token_cls.Identifier, 'identity'), using_token_or_form]
        )

        _ = []

        for an_item in evaluated_coll_or_nexc.items():
            local_env[identifier_token.dt().origin()] = an_item
            evaluated_or_a_nexc = eval_function(local_env, using_token_or_form)
            if isinstance(evaluated_or_a_nexc, datatypes.NException):
                return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Proxy, evaluated_or_a_nexc)]
            _.append(evaluated_or_a_nexc)

        _resulting_vector_data_type = datatypes.Vector(tuple(_))

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Proxy, _resulting_vector_data_type)]

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'let',
           'type': 'macro',
           'forms': ['(let [b1 v1 ...] b1)'],
           'docstring': 'Allows to define local binding pairs and access them later'})
    def let_macro(token_cls,
                  tree: list,
                  local_env: dict,
                  _,
                  eval_function) -> list:
        """
        Builtin 'let' macro implementation

        :param token_cls: nanamilang.token.Token class
        :param tree: slice of tree eval_func has encountered
        :param local_env: local environment during expr eval
        :param _: unused argument, but i need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        bindings_form, body_form = tree

        NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS_EVEN(bindings_form, 'let: bindings form needs to be even')

        for [key_token_or_form, value_token_or_form] in NML_M_ITERATE_AS_PAIRS(bindings_form, 2):
            evaluated = eval_function(
                local_env,
                value_token_or_form
                if isinstance(value_token_or_form, list)
                else [token_cls(token_cls.Identifier, 'identity'), value_token_or_form])
            if isinstance(evaluated, datatypes.NException):
                return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Proxy, evaluated)]
            if isinstance(key_token_or_form, list):
                NML_M_ASSERT_FORM_IS_A_VECTOR(key_token_or_form, 'let: left-side needs to be a Vector form')
                assert isinstance(evaluated, datatypes.Vector), 'let: right-side needs to be a Vector data type'
                NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS(
                    key_token_or_form,
                    evaluated.count().reference(), 'let: lengths of left- and right-side vectors are mismatching')
                for from_left, from_right in zip(NML_M_ITERATE_AS_PAIRS(key_token_or_form), evaluated.reference()):
                    assert from_left.type() == token_cls.Identifier, 'let: the left-side needs to be an Identifier'
                    local_env[from_left.dt().origin()] = from_right
            else:
                assert key_token_or_form.type() == token_cls.Identifier, 'let: the left-side needs to be Identifier'
                local_env[key_token_or_form.dt().origin()] = evaluated

        return body_form if isinstance(body_form, list) else [token_cls(token_cls.Identifier, 'identity'), body_form]

    #################################################################################################################


class BuiltinFunctions:
    """NanamiLang Builtin Functions"""

    #################################################################################################################

    @staticmethod
    def install(fn_meta: dict, fn_callback) -> bool:
        """
        Allow others to install own functions.
        For example: let the REPL install (exit) function

        :param fn_meta: required function meta information
        :param fn_callback: installed function callback reference
        """

        reference_key = f'{fn_meta.get("name")}_func'
        maybe_existing = getattr(BuiltinFunctions, reference_key, None)
        if maybe_existing:
            delattr(BuiltinFunctions, reference_key)

        setattr(BuiltinFunctions, reference_key, fn_callback)
        getattr(BuiltinFunctions, reference_key, None).meta = fn_meta
        return bool(getattr(BuiltinFunctions, reference_key, None).meta == fn_meta)

    #################################################################################################################

    cached = {}

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """Resolve function by its name"""

        if fun := BuiltinMacros.cached.get(fn_name, {}):
            return fun
        for func in BuiltinFunctions.functions():
            if func.meta.get('name') == fn_name:
                resolved: dict = {'function_name': fn_name,
                                  'function_reference': func}
                BuiltinFunctions.cached.update({fn_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinFunctions.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _func functions"""

        attrib_names = filter(lambda _: '_func' in _, BuiltinFunctions().__dir__())

        return list(map(lambda n: getattr(BuiltinFunctions, n, None), attrib_names))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'identity',
           'type': 'function',
           'forms': ['(identity something)'],
           'docstring': 'Returns something as it is'})
    def identity_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'identity' function implementation

        :param args: incoming 'identity' function arguments
        :return: datatypes.Base

        """

        return args[0]
        # Function is required for internal purposes && can be used elsewhere

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Collection, datatypes.Base]]]],
           'name': 'contains?',
           'type': 'function',
           'forms': ['(contains? collection element)'],
           'docstring': 'Check whether collection contains element or not'})
    def contains_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'contains?' function implementation

        :param args: incoming 'contains?' function arguments
        :return: datatypes.Base

        TODO: this function could be moved to 'stdlib.nml' (requires ArgumentsTypeChainVariants spec in defn)
        """

        collection: datatypes.Collection
        element: datatypes.Base

        collection, element = args

        return collection.contains(element)
        # Since complex data structures use Boolean to represent boolean value, there is no need to cast it manually

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.HashSet, datatypes.Base],
                                                       [datatypes.Vector, datatypes.IntegerNumber],
                                                       [datatypes.HashMap, datatypes.Base],
                                                       [datatypes.NException, datatypes.Keyword]]]],
           'name': 'get',
           'type': 'function',
           'forms': ['(get collection by)'],
           'docstring': 'Returns collection element by key, index or element'})
    def get_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'get' function implementation

        :param args: incoming 'get' function arguments
        :return: datatypes.Base

        TODO: this function could be moved to 'stdlib.nml' (requires ArgumentsTypeChainVariants spec in defn)
        """

        collection: datatypes.Collection
        by: datatypes.Base

        collection, by = args

        return collection.get(by)
        # Let the concrete Collection.get() handle 'get' operation depending on what collection is and 'by' argument

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-vector',
           'type': 'function',
           'forms': ['(make-vector e1 e2 ... eX)'],
           'docstring': 'Creates a Vector data structure'})
    def make_vector_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'make-vector' function implementation

        :param args: incoming 'make-vector' function arguments
        :return: datatypes.Vector
        """

        return datatypes.Vector(tuple(args))
        # Let the Collection.__init__() handle vector structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-hashset',
           'type': 'function',
           'forms': ['(make-hashset e1 e2 ... eX)'],
           'docstring': 'Creates a HashSet data structure'})
    def make_set_func(args: List[datatypes.Base]) -> datatypes.HashSet:
        """
        Builtin 'make-hashset' function implementation

        :param args: incoming 'make-hashset' function arguments
        :return: datatypes.HashSet
        """

        return datatypes.HashSet(tuple(args))
        # Let the Collection.__init__() handle hashset structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'make-hashmap',
           'type': 'function',
           'forms': ['(make-hashmap k1 v2 ... kX vX)'],
           'docstring': 'Creates a HashMap data structure'})
    def make_hashmap_func(args: List[datatypes.Base]) -> datatypes.HashMap:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'make-hashmap' function arguments
        :return: datatypes.HashMap
        """

        return datatypes.HashMap(tuple(args))
        # Let the Collection.__init__() handle hashmap structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'not',
           'type': 'function',
           'forms': ['(not something)'],
           'docstring': 'Returns something truth inverted'})
    def not_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'not' function implementation

        :param args: incoming 'not' function arguments
        :return: datatypes.String
        """

        return datatypes.Boolean(args[0].truthy()).nope()
        # We need to cast truthy() return value manually to Boolean

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '=',
           'type': 'function',
           'forms': ['(= s1 s2 ... sX)'],
           'docstring': 'Returns false once current != next'})
    def eq_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin '=' function implementation

        :param args: incoming '=' function arguments
        :return: datatypes.Boolean
        """

        _ne = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _ne = curr.hashed() == _next.hashed()
            if not _ne:
                break

        return datatypes.Boolean(_ne)  # once _ne == False, exit the function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<',
           'type': 'function',
           'forms': ['(< n1 n2 ... nX)'],
           'docstring': 'Returns false once current > than next'})
    def less_than_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<' function implementation

        :param args: incoming '<' function arguments
        :return: datatypes.Boolean
        """

        _lt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lt = curr.reference() < _next.reference()
            if not _lt:
                break

        return datatypes.Boolean(_lt)  # once _lt == False, exit the function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>',
           'type': 'function',
           'forms': ['(> n1 n2 ... nX)'],
           'docstring': 'Returns false once current < than next'})
    def greater_than_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>' function implementation

        :param args: incoming '>' function arguments
        :return: datatypes.Boolean
        """

        _gt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gt = curr.reference() > _next.reference()
            if not _gt:
                break

        return datatypes.Boolean(_gt)  # once _gt == False, exit the function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<=',
           'type': 'function',
           'forms': ['(<= n1 n2 ... nX)'],
           'docstring': 'Returns false once current >= than next'})
    def less_than_eq_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        _lte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lte = curr.reference() <= _next.reference()
            if not _lte:
                break

        return datatypes.Boolean(_lte)  # once _lte == False, exit the function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>=',
           'type': 'function',
           'forms': ['(>= n1 n2 ... nX)'],
           'docstring': 'Returns false once current <= than next'})
    def greater_than_eq_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        _gte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gte = curr.reference() >= _next.reference()
            if not _gte:
                break

        return datatypes.Boolean(_gte)  # once _gte == False, exit the function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '+',
           'type': 'function',
           'forms': ['(+ n1 n2 ... nX)'],
           'docstring': 'Applies "+" operation to passed numbers'})
    def add_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '+' function implementation

        :param args: incoming '+' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ + x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '-',
           'type': 'function',
           'forms': ['(- n1 n2 ... nX)'],
           'docstring': 'Applies "-" operation to passed numbers'})
    def sub_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '-' function implementation

        :param args: incoming '-' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ - x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '*',
           'type': 'function',
           'forms': ['(* n1 n2 ... nX)'],
           'docstring': 'Applies "*" operation to passed numbers'})
    def mul_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '*' function implementation

        :param args: incoming '*' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ * x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '/',
           'type': 'function',
           'forms': ['(/ n1 n2 ... nX)'],
           'docstring': 'Applies "/" operation to passed numbers'})
    def divide_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '/' function implementation

        :param args: incoming '/' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ / x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'mod',
           'type': 'function',
           'forms': ['(mod n1 n2 ... nX)'],
           'docstring': 'Applies "mod" operation to passed numbers'})
    def modulo_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin 'mod' function implementation

        :param args: incoming 'mod' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ % x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'map',
           'type': 'function',
           'forms': ['(map function collection)'],
           'docstring': 'Allows to map collection elements with the passed function'})
    def map_func(args: List[datatypes.Base]) -> datatypes.Vector or datatypes.NException:
        """
        Builtin 'map' function implementation

        :param args: incoming 'map' function arguments
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        _ = []
        for element in collection.items():
            res = function.reference()([element])
            if isinstance(res, datatypes.NException):
                return res  # <- if we encountered an NException data type, we need to propagate it
            _.append(res)

        return datatypes.Vector(tuple(_))  # <- return a resulting vector of the mapped collection elements

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'filter',
           'type': 'function',
           'forms': ['(filter function collection)'],
           'docstring': 'Allows to filter collection elements with the passed function'})
    def filter_func(args: List[datatypes.Base]) -> datatypes.Vector or datatypes.NException:
        """
        Builtin 'filter' function implementation

        :param args: incoming 'filter' function arguments
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        _ = []
        for element in collection.items():
            res = function.reference()([element])
            if isinstance(res, datatypes.NException):
                return res  # <- if we encountered an NException data type, we need to propagate it
            if res.truthy():
                _.append(element)

        return datatypes.Vector(tuple(_))  # <- return a resulting vector of the filtered collection elements
