#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library.py                                                              #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 3.0 Library class                                                                         #
#                                                                                                 #
###################################################################################################

"""Base class for macal Library"""

from .macal_lextoken import LexToken
from .macal_lextokentypes import LPAREN
from .macal_variable_types import ANY, PARAMS
from .macal_parsernodes import ast_Block, ast_function_Param_list
from .macal_astvariablenode import ast_Variable
from .macal_function import MacalFunction
from .macal_scope import MacalScope
from .macal_exceptions import (InvalidFunctionCallException, InvalidParamCountException, 
                              MissingParameterException, InvalidParamTypeException,
                              VariableNotFoundException)
from .macal_interpreterconsts import FuncArg
from .macal_variable import MacalVariable

class MacalLibrary:
    """Base class for Libraries"""
    def __init__(self, name):
        self.name : str = name
        self.functions : list[MacalFunction] = []
        self.variables : list[MacalVariable] = []
        self.version : str = "3.0.0"

    def CreateArg(self, name: str, param_type: str):
        """Create a new parameter for the function"""
        return ast_Variable(LexToken(param_type, name, -1, -1, -1))

    def RegisterFunction(self, name: str, args: list[FuncArg], call_func):
        """Register a new function with the library."""
        prms = ast_function_Param_list(LexToken(LPAREN, '(', -1, -1, -1))
        for arg in args:
            prms.params.append(self.CreateArg(arg.arg_name, arg.arg_type))
        fun = MacalFunction(name, prms, ast_Block(None))
        fun.is_extern = True
        fun.call_extern = call_func
        self.functions.append(fun)

    def variable_by_name(self, name: str) -> MacalVariable:
        return next((x for x in self.variables if x.name == name), None)

    def register_variable(self, name: str, value):
        var = self.variable_by_name(name)
        if var is not None:
            raise RuntimeError(f"Invalid register variable ({name}), variable already exists", -1, -1)
        var = MacalVariable(name)
        var.set_value(value)
        var.set_type(MacalScope.get_value_type(value))
        self.variables.append(var)

    def ValidateFunction(self, name: str, fn: MacalFunction, scope: MacalScope):
        """Validate if the function exists."""
        if name != fn.name:
            raise InvalidFunctionCallException(name, fn, scope)
        return True

    def ParamByName(self, lst: list, name: str):
        """Retrieves an item from the list based on its name"""
        return next((x for x in lst if x.name == name), None)

    def ValidateParams(self, name: str, params: list, scope: MacalScope, func: MacalFunction):
        """Validate if all the parameters that where passed are correct."""
        funcparams = func.args
        if len(params) != len(funcparams.params):
            raise InvalidParamCountException(name, scope, len(params), len(funcparams.params))
        for funcparam in funcparams.params:
            param = self.ParamByName(params, funcparam.token.token_value)
            if param is None:
                raise MissingParameterException(name, scope, funcparam.token.token_value, func.name)
            pt = param.get_type()
            if pt != funcparam.token.token_type and funcparam.token.token_type != ANY and funcparam.token.token_type != PARAMS and pt != ANY:
                raise InvalidParamTypeException(name, scope, funcparam.token.token_value, pt, funcparam.token.token_type);
        return True

    def GetParamValue(self, params: list, name: str):
        """Get the value from a parameter in the params list."""
        param = self.ParamByName(params, name)
        if param is None:
            raise MissingParameterException(self.name, None, name)
        value = param.get_value()
        return value

    def GetVariableFromParam(self, params: list, scope: MacalScope, name: str):
        """Get a scope variable from a parameter on the parameters list."""
        pv = self.GetParamValue(params, name)
        var = scope.find_variable(pv.name)
        if var is None:
            raise VariableNotFoundException(pv.name, scope)
        return var, pv.index

    def GetIndexedVariableValue(self, var, index):
        value = var.get_value()
        for idx in index:
            value = value[idx.value]
        return value

    def GetFunction(self, name: str):
        """Find function by name"""
        return next((x for x in self.functions if x.name == name), None)
