from app.kit.html import Attr, Element, Page, Tag
from app.kit.layouts import Base


class ListItemsPage(Page):
    def __init__(self) -> None:
        self.doc = Base.model_copy()
        self.doc.title = "fullstack-python-example!"
        self.doc.body = [
            Element(
                tag=Tag.div,
                attrs={Attr._id: "listItemTarget"},
                children=[
                    Element(
                        tag=Tag.h1,
                        attrs={Attr._id: "title", Attr._class: "text-4xl"},
                        innerHTML="list items",
                    ),
                    Element(
                        tag=Tag.p,
                        children=[
                            "This is a list of items.",
                        ],
                    ),
                    Element(
                        tag=Tag.p,
                        children=[
                            "Add a new item ",
                            Element(
                                tag=Tag.a,
                                attrs={
                                    "href": "/items/new",
                                    Attr._class: "underline font-bold "
                                    "hover:text-blue-500",
                                },
                                children=["here"],
                            ),
                            ".",
                        ],
                    ),
                ],
            )
        ]
