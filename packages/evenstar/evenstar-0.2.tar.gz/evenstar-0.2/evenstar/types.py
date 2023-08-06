import json
from typing import Any, Dict, List, Optional, Union


class Enum(str):
    """Exact and pure a subclass of str to represent Enum type in Arguments

    Examples:
        >>> Enum("ACCEPT")
        'ACCEPT'
        >>> args = Arguments({"state": Enum("ACCEPTED")})
    """

    pass


class VarSymbol(str):
    """Exact and pure a subclass of str to represent variables in Arguments

    Examples:
        >>> VarSymbol("$student_id")
        '$student_id'
        >>> args = Arguments({"id": VarSymbol("$student_id")})
    """

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
    """Represents an inline-fragment

    Args:
        on (str): type on the thing that this fragment will be applied on,
            like "HUMAN"
        children (List[Union[str, Field]]): List of fields
            (having at least one child is necessary)

    Attributes:
        on (str): type on the thing that this fragment will be applied on,
            like "HUMAN"
        children (List[Union[str, Field]]): List of fields

    Examples:
        >>> print(InlineFragment(on="HUMAN", children=["name", "age"]).render())
        ... on HUMAN {
          name
          age
        }
        >>> on_human = InlineFragment(
            on="HUMAN",
            children=["name", Field("age", alias="years")]
        )
    """  # noqa: E501

    def __init__(
        self, on: str, children: List[Union[str, "Field"]],
    ):
        if not children:
            raise ValueError("InlineFragment must have at least one child.")
        self.on = on
        self.children = children

    def render(self, json_encoder: Any = None, indent: int = 0) -> str:
        spaces = indent * " "
        if not self.children:
            raise ValueError("InlineFragment must have at least one child.")
        result = "... on %s {\n" % self.on
        for c in self.children:
            if isinstance(c, str):
                result += "{spaces}{field}\n".format(spaces=spaces, field=c)
            elif isinstance(c, Field):
                for line in c.render(json_encoder, indent).split("\n"):
                    result += "{spaces}{field}\n".format(
                        spaces=spaces, field=line
                    )
            else:
                raise TypeError(
                    "InlineFragment's children must be Field or str,"
                    "you passed: %s" % (type(c))
                )
        result += "}"
        return result


class Arguments(object):
    """Represents arguments of a field

    Args:
        data (Dict[str, Any]): just the data, the arguments,
            a dictionary with at least one memeber

    Attributes:
        data (Dict[str, Any]): just the data, the arguments,
            a dictionary with at least one memeber

    Examples:
        >>> args = Arguments(
            {
                "a": 1,
                "b": 2.123,
                "c": False,
                "d": None,
                "e": "Black!",
                "f": Enum("APPLE"),
                "g": VarSymbol("$count"),
            }
        )
        >>> Field("blah", arguments=args).render()
        'blah(a: 1, b: 2.123, c: false, d: null, e: "Black!", f: APPLE, g: $count)'
    """  # noqa: E501

    def __init__(self, data: Dict[str, Any]):
        if not data:
            raise ValueError("Arguments must have at least one member.")
        self.data = data

    def render(self, json_encoder: Any = None) -> str:
        if not self.data:
            raise ValueError("Arguments must have at least one member.")

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
                rendered_value = json.dumps(v, cls=json_encoder)
            return rendered_value

        s = ""
        for key, value in self.data.items():
            s += "%s: %s, " % (str(key), r(value))
        return s[:-2] if s.endswith(", ") else s


class Field(object):
    """Represents a field

    Args:
        name (str): Name of field
        alias (:obj:`Optional[str]`, optional): Alias of the field (like `car: automobile`),
            default is `None`.
        arguments (:obj:`Optional[Arguments]`, optional): Arguments (Defualt is `None`)
        children: (:obj:`Optional[List[Union[Field, InlineFragment, str]]]`, optional):
            List of members (inner fields), a member can be another Field,
            a InlineFragment or a str, default is `None`

    Attributes:
        name (str): Name of field
        alias (:obj:`Optional[str]`, optional): Alias of the field (like `car: automobile`)
        arguments (:obj:`Optional[Arguments]`, optional): Arguments
        children: (:obj:`Optional[List[Union[Field, InlineFragment, str]]]`, optional):
            List of members (inner fields), a member can be another Field,
            a InlineFragment or a str.

    Examples:
        >>> Field("blah").render()
        'blah'
        >>> Field("blah", "something_else").render()
        'something_else: blah'
        >>> Field("blah", alias="something_else", arguments=Arguments({"id": 12})).render()
        'something_else: blah(id: 12)'
        >>> my_field = Field(
            "blah",
            alias="something_else",
            arguments=Arguments({"id": 12}),
            children=["c1", Field("c2", alias="ccc")]
        )
        >>> print(my_field.render())
        something_else: blah(id: 12) {
            c1
            ccc: c2
        }
    """  # noqa: E501

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

    def render(self, json_encoder: Any = None, indent: int = 0) -> str:
        spaces = indent * " "
        result = ""
        if self.alias:
            result += "%s: " % self.alias
        result += self.name
        if self.arguments:
            result += "(%s)" % self.arguments.render(json_encoder)
        if self.children:
            result += " {\n"
            for c in self.children:
                if isinstance(c, str):
                    result += "{spaces}{field}\n".format(
                        spaces=spaces, field=c
                    )
                elif isinstance(c, (InlineFragment, Field)):
                    for line in c.render(json_encoder, indent).split("\n"):
                        result += "{spaces}{field}\n".format(
                            spaces=spaces, field=line
                        )
                else:
                    raise TypeError(
                        "Fields's children must be Field or InlineFragment"
                        " or str, you passed: %s" % (type(c))
                    )
            result += "}"
        return result


class Query(object):
    """Represents a query operation

    Args:
        name (:obj:`Optional[str]`, optional): Name of the operation,
            default is `None`
        children (`List[Union[Field, str]]`):
            List of members, a member can be a Field or a str.
        variables (:obj:`Optional[List[VarDeclaration]]`, optional):
            You can define variables of the query operation here.
            Default is `None`

    Attributes:
        name (:obj:`Optional[str]`, optional): Name of the operation.
        children (`List[Union[Field, str]]`):
            List of members, a member can be a Field or a str.
        variables (:obj:`Optional[List[VarDeclaration]]`, optional):
            You can define variables of the query operation here.
    """

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

    def render(self, json_encoder: Any = None, indent: int = 0) -> str:
        spaces = indent * " "

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
                    variables_q += " = %s" % json.dumps(
                        v.default, cls=json_encoder
                    )
                if index != len(self.variables) - 1:
                    variables_q += ", "
            variables_q += ")"
            result += variables_q

        # Add children (fields)
        result += " {\n"
        for c in self.children:
            if isinstance(c, str):
                result += "{spaces}{field}\n".format(spaces=spaces, field=c)
            elif isinstance(c, Field):
                for line in c.render(json_encoder, indent).split("\n"):
                    result += "{spaces}{field}\n".format(
                        spaces=spaces, field=line
                    )
            else:
                raise TypeError(
                    "Operation's children must be Field or str,"
                    " you passed: %s" % (type(c))
                )
        # Close
        result += "}"
        return result


class Mutation(Query):
    """Represents a mutation operation

    Args:
        name (:obj:`Optional[str]`, optional): Name of the operation,
            default is `None`.
        children (`List[Union[Field, str]]`):
            List of members, a member can be a Field or a str.
        variables (:obj:`Optional[List[VarDeclaration]]`, optional):
            You can define variables of the mutation operation here.
            Default is `None`

    Attributes:
        name (:obj:`Optional[str]`, optional): Name of the operation.
        children (`List[Union[Field, str]]`):
            List of members, a member can be a Field or a str.
        variables (:obj:`Optional[List[VarDeclaration]]`, optional):
            You can define variables of the mutation operation here.
    """

    keyword = "mutation"


class Request(object):
    """A whole request including query, variables and operation name

    Args:
        operation_name (:obj:`Optional[str]`, optional): name of the operation which
            we want to execute, default is `None`.
        children (`List[Union[Mutation, Query]]`):
            List of members, queries and mutations.
        variables (Dict[str, Any]): Variables

    Attributes:
        operation_name (:obj:`Optional[str]`, optional): name of the operation which
            we want to execute.
        children (`List[Union[Mutation, Query]]`):
            List of members, queries and mutations.
        variables (Dict[str, Any]): Variables

    Examples:
        >>> q = Query(...)
        >>> req = Request(
            children=[q],
            variables={
                "basket_create_params": {
                    "id": 123,
                    "time": 1634297081,
                },
            },
        )
        >>> requests.post(
            "http://localhost/graphql,
            data=json.dumps(req.json()),
            headers={"Content-Type": "application/json"},
        )
    """  # noqa: E501

    def __init__(
        self,
        children: List[Union[Mutation, Query]],
        variables: Dict[str, Any],
        operation_name: Optional[str] = None,
    ):
        self.children = children
        self.operation_name = operation_name
        self.variables = variables

    def json(
        self, json_encoder: Any = None, indent: int = 0
    ) -> Dict[str, Any]:
        """This function renders everthing and puts to togather
        query, operation name and variables to create a dictionary
        which you can dump it as a request body.

        Args:
            json_encoder (:obj:`Any`, optional): A json encoder class,
                default is `None`
            indent (:obj:`int`, optional): Spance count as indent,
                it's usefull for pretty printing, default is `0`
        Returns:
            Dict[str, Any]: GraphQL request body as a dictionary
        """
        result: Dict[str, Any] = {
            "query": "\n\n".join(
                [c.render(json_encoder, indent) for c in self.children]
            )
        }
        if self.operation_name:
            result["operationName"] = self.operation_name
        if self.variables:
            result["variables"] = self.variables
        return result
