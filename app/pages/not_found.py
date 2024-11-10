from app.kit.html import Attr, Element, Page, Tag
from app.kit.layouts import Base


class NotFoundPage(Page):
    def __init__(self) -> None:
        self.doc = Base.model_copy()
        self.doc.title = "fullstack-python-example!"
        self.doc.body = [
            Element(
                tag=Tag.h1,
                attrs={Attr._id: "title", Attr._class: "text-4xl"},
                innerHTML="not found 😱",
            ),
            Element(
                tag=Tag.p,
                children=[
                    "what on earth are you looking for? ",
                    Element(
                        tag=Tag.a,
                        attrs={
                            "href": "/",
                            Attr._class: "underline font-bold hover:text-blue-500",
                        },
                        children=["go home! 🏠"],
                    ),
                ],
            ),
        ]
