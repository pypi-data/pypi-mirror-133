import dataclasses
import typing

from dataclasses_jsonschema import JsonSchemaMixin
from django.core.paginator import Paginator
from django.http import HttpRequest


def iterable_factory(item_cls, paginate=False, page_size=10):
    """A factory for processing iterable results.

    Generates a dynamic dataclass wrapper that can facilitate
    returning iterable results of items and paginated results.
    """

    class Wrapper:
        items: typing.List[item_cls]
        request: dataclasses.InitVar[HttpRequest] = None
        page: int = dataclasses.field(init=False)
        count: int = dataclasses.field(init=False)

        def __post_init__(self, request):
            if paginate:
                page_number = int(request.GET.get("page", 1))
                paginator = Paginator(self.items, page_size)
                page = paginator.get_page(page_number)
                self.page = page_number
                self.count = paginator.count
                self.items = page.object_list
            else:
                self.page = 1
                self.count = len(self.items)

    new_cls = type(
        f"Iterable[{item_cls.__name__}]",
        (Wrapper, JsonSchemaMixin),
        dict(Wrapper.__dict__),
    )
    new_cls.__doc__ = f"An Iterable of {item_cls.__name__} items."
    return dataclasses.dataclass(new_cls)
