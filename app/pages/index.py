from app.kit.html import Attr, Element, Page, Tag
from app.kit.layouts import Base


class IndexPage(Page):
    def __init__(self) -> None:
        self.doc = Base.model_copy()
        self.doc.title = "fullstack-python-example!"
        self.doc.body = [
            Element(
                tag=Tag.h1,
                attrs={Attr._id: "title", Attr._class: "text-4xl"},
                innerHTML="fullstack-python-example!",
            ),
            Element(
                tag=Tag.p,
                children=[
                    "This is a FastAPI project that uses the ",
                    Element(
                        tag=Tag.a,
                        attrs={
                            "href": "https://fastapi.tiangolo.com",
                            "target": "blank",
                        },
                        children=["fastapi"],
                    ),
                    " framework.",
                ],
            ),
            Element(
                tag=Tag.p,
                children=[
                    "You can view our items ",
                    Element(
                        tag=Tag.a,
                        attrs={
                            "href": "/items",
                            Attr._class: "underline font-bold hover:text-blue-500",
                        },
                        children=["here"],
                    ),
                    ".",
                ],
            ),
            Element(
                tag=Tag.p,
                children=[
                    "You can add a new item ",
                    Element(
                        tag=Tag.a,
                        attrs={
                            "href": "/items/new",
                            Attr._class: "underline font-bold hover:text-blue-500",
                        },
                        children=["here"],
                    ),
                    ".",
                ],
            ),
        ]
