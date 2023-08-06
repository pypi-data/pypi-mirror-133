import functools
from typing import Any, Callable, List, Literal, Optional, Sequence, Type, Union

from django.db import transaction
from strawberry.arguments import UNSET
from strawberry.permission import BasePermission
from strawberry.schema_directive import StrawberrySchemaDirective
from strawberry_django.mutations.fields import get_input_data, update_m2m

from strawberry_django_plus.resolvers import callable_resolver

from .fields import StrawberryDjangoField, field

subscription = functools.partial(field, is_subscription=True)

mutation = field()


def create_resolver(f: StrawberryDjangoField, data: Any):
    input_data = get_input_data(f.input_type, data)
    instance = f.model.objects.create(**input_data)
    update_m2m([instance], data)
    return instance


def update_resolver(f: StrawberryDjangoField, data: Any, **kwargs):
    queryset = f.model.objects.all()
    queryset = f.get_queryset(queryset=queryset, info=info, data=data, **kwargs)
    input_data = get_input_data(f.input_type, data)
    queryset.update(**input_data)
    update_m2m(queryset, data)
    return queryset


def create(
    input_type: Any,
    *,
    name: Optional[str] = None,
    field_name: Optional[str] = None,
    description: Optional[str] = None,
    permission_classes: Optional[List[Type[BasePermission]]] = None,
    deprecation_reason: Optional[str] = None,
    directives: Optional[Sequence[StrawberrySchemaDirective]] = (),
):
    f = field(
        name=name,
        field_name=field_name,
        description=description,
        permission_classes=permission_classes,
        deprecation_reason=deprecation_reason,
        directives=directives,
    )

    @callable_resolver
    @transaction.atomic
    def resolver(input: input_type):  # noqa:A002
        if f.is_list:
            return [create_resolver(f, d) for d in input]

        return create_resolver(f, input)

    return f(resolver)


def update(
    input_type: Any,
    *,
    name: Optional[str] = None,
    field_name: Optional[str] = None,
    filters: Any = UNSET,
    description: Optional[str] = None,
    permission_classes: Optional[List[Type[BasePermission]]] = None,
    deprecation_reason: Optional[str] = None,
    directives: Optional[Sequence[StrawberrySchemaDirective]] = (),
):

    f = field(
        name=name,
        field_name=field_name,
        filters=filters,
        description=description,
        permission_classes=permission_classes,
        deprecation_reason=deprecation_reason,
        directives=directives,
    )

    @callable_resolver
    @transaction.atomic
    def resolver(input: input_type):  # noqa:A002

        if f.is_list:
            return [create_resolver(f, d) for d in input]

        return create_resolver(f, input)

    return f(resolver)


def delete(
    input_type: Any,
    *,
    name: Optional[str] = None,
    field_name: Optional[str] = None,
    filters: Any = UNSET,
    description: Optional[str] = None,
    permission_classes: Optional[List[Type[BasePermission]]] = None,
    deprecation_reason: Optional[str] = None,
    directives: Optional[Sequence[StrawberrySchemaDirective]] = (),
):
    return field(
        name=name,
        field_name=field_name,
        filters=filters,
        description=description,
        permission_classes=permission_classes,
        deprecation_reason=deprecation_reason,
        directives=directives,
    )
