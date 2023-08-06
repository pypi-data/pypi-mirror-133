from typing import Dict, List, Union, Any, Optional
import json


class Enum(str):
    pass


class VarSymbol(str):
    pass


class _EmptyCls(object):
    pass


Empty = _EmptyCls()


class VarDeclaration(object):
    def __init__(
        self,
        name,
        type: str,
        default: Union[str, float, int, None, bool, Enum, _EmptyCls] = Empty,
    ):
        self.name, self.type, self.default = name, type, default


class InlineFragment(object):
    def __init__(
        self, on: str, children: List[Union[str, "Field"]],
    ):
        if not children:
            raise ValueError("InlineFragment must have at least one child.")
        self.on = on
        self.children = children

    def render(self) -> str:
        result = "... on %s {\n" % self.on
        for c in self.children:
            if isinstance(c, str):
                result += "%s\n" % c
            elif isinstance(c, Field):
                result += "%s\n" % c.render()
            else:
                raise TypeError(
                    "InlineFragment's children must be Field or str,"
                    "you passed: %s" % (type(c))
                )
        result += "}"
        return result


class Arguments(object):
    def __init__(self, data: Dict[str, Any]):
        if not data:
            raise ValueError("Arguments must have at least one member.")
        self._data = data

    def render(self) -> str:
        def r(v):
            if isinstance(v, Enum) or isinstance(v, VarSymbol):
                rendered_value = v
            elif isinstance(v, tuple) or isinstance(v, list):
                rendered_value = "["
                for index, member in enumerate(v):
                    rendered_value += str(r(member))
                    if index != len(v) - 1:
                        rendered_value += ", "
                rendered_value += "]"
            elif isinstance(v, dict):
                rendered_value = "{"
                for inner_key, inner_value in v.items():
                    rendered_value += "%s: %s, " % (
                        str(inner_key),
                        r(inner_value),
                    )
                if rendered_value.endswith(", "):
                    rendered_value = rendered_value[:-2]
                rendered_value += "}"
            else:
                rendered_value = json.dumps(v)
            return rendered_value

        s = ""
        for key, value in self._data.items():
            s += "%s: %s, " % (str(key), r(value))
        return s[:-2] if s.endswith(", ") else s


class Field(object):
    def __init__(
        self,
        name: str,
        alias: Optional[str] = None,
        arguments: Optional[Arguments] = None,
        children: Optional[List[Union["Field", "InlineFragment", str]]] = None,
    ):
        self.name = name
        self.alias = alias
        self.arguments = arguments
        self.children = children

    def render(self) -> str:
        result = ""
        if self.alias:
            result += "%s: " % self.alias
        result += self.name
        if self.arguments:
            result += "(%s)" % self.arguments.render()
        if self.children:
            result += " {\n"
            for c in self.children:
                if isinstance(c, str):
                    result += "%s\n" % c
                elif isinstance(c, (InlineFragment, Field)):
                    result += "%s\n" % c.render()
                else:
                    raise TypeError(
                        "Fields's children must be Field or InlineFragment"
                        " or str, you passed: %s" % (type(c))
                    )
            result += "}"
        return result


class Query(object):

    keyword = "query"

    def __init__(
        self,
        children: List[Union["Field", str]],
        name: Optional[str] = None,
        variables: Optional[List[VarDeclaration]] = None,
    ):
        if not children:
            raise ValueError(
                "Query and Mutation must have at least one child."
            )
        self.name = name
        self.children = children
        self.variables = variables

    def render(self) -> str:
        # Open
        result = "%s" % self.keyword
        # Add name
        if self.name:
            result += " %s" % self.name
        # Add variables
        if self.variables:
            variables_q = " ("
            for index, v in enumerate(self.variables):
                variables_q += "%s: %s" % (v.name, v.type)
                if isinstance(v.default, Enum) or isinstance(
                    v.default, VarSymbol
                ):
                    variables_q += " = %s" % v.default
                elif isinstance(v.default, _EmptyCls):
                    pass
                else:
                    variables_q += " = %s" % json.dumps(v.default)
                if index != len(self.variables) - 1:
                    variables_q += ", "
            variables_q += ")"
            result += variables_q

        # Add children (fields)
        result += " {\n"
        for c in self.children:
            if isinstance(c, str):
                result += "%s\n" % c
            elif isinstance(c, Field):
                result += "%s\n" % c.render()
            else:
                raise TypeError(
                    "Operation's children must be Field or str,"
                    " you passed: %s" % (type(c))
                )
        # Close
        result += "}"
        return result


class Mutation(Query):

    keyword = "mutation"


class Request(object):
    def __init__(
        self,
        children: List[Union[Mutation, Query]],
        variables: Dict[str, Any],
        operation_name: Optional[str],
    ):
        self.children = children
        self.operation_name = operation_name
        self.variables = variables

    def json(self) -> Dict[str, Any]:
        result = {"query": "\n\n".join([c.render() for c in self.children])}
        if self.operation_name:
            result["operationName"] = self.operation_name
        if self.variables:
            result["variables"] = self.variables
        return result
