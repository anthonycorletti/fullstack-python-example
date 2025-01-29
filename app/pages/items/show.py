from app.kit.html import Attr, Element, InputType, Page, Tag
from app.kit.layouts import Base
from app.models.items import Items


class ShowItemPage(Page):
    def __init__(self, data: Items) -> None:
        self.doc = Base.model_copy()
        self.doc.title = "show item"
        self.doc.body = [
            Element(
                tag=Tag.div,
                attrs={Attr._id: "updateItemTarget"},
                children=[
                    Element(
                        tag=Tag.h1,
                        innerHTML=f"item: {data.name}",
                        attrs={Attr._class: "text-4xl pb-2"},
                    ),
                    Element(
                        tag=Tag.form,
                        attrs={
                            Attr.hx_put: f"/items/{data.name}",
                            Attr.hx_ext: "json-enc",
                            Attr.hx_target: "#updateItemTarget",
                            Attr.hx_swap: "outerHTML",
                        },
                        children=[
                            Element(
                                tag=Tag.input,
                                attrs={
                                    Attr._type: InputType.text.value,
                                    "name": "name",
                                    Attr.placeholder: "the item name",
                                    Attr.required: "",
                                    Attr._class: "bg-transparent border-b-2 "
                                    "border-blue-500 focus:outline-none "
                                    "focus:border-blue-700",
                                    Attr.value: data.name,
                                },
                            ),
                            Element(
                                tag=Tag.br,
                            ),
                            Element(
                                tag=Tag.input,
                                attrs={
                                    Attr._type: InputType.number.value,
                                    "name": "count",
                                    Attr.placeholder: "how many?",
                                    Attr.required: "",
                                    Attr._class: "bg-transparent border-b-2 "
                                    "border-blue-500 focus:outline-none "
                                    "focus:border-blue-700",
                                    Attr.value: data.count,
                                },
                            ),
                            Element(
                                tag=Tag.br,
                            ),
                            Element(
                                tag=Tag.input,
                                attrs={
                                    Attr._type: InputType.text.value,
                                    "name": "description",
                                    Attr.placeholder: "some more details...",
                                    Attr._class: "bg-transparent border-b-2 "
                                    "border-blue-500 focus:outline-none "
                                    "focus:border-blue-700",
                                    Attr.value: data.description,
                                },
                            ),
                            Element(
                                tag=Tag.br,
                            ),
                            Element(
                                tag=Tag.input,
                                attrs={
                                    Attr._type: InputType.submit.value,
                                    Attr.value: "Update",
                                    Attr._class: "bg-blue-500 hover:bg-blue-700 "
                                    "text-white font-bold py-2 px-4 rounded",
                                },
                            ),
                            Element(
                                tag=Tag.button,
                                attrs={
                                    Attr.hx_delete: f"/items/{data.name}",
                                    Attr.hx_confirm: "Are you sure?",
                                    Attr._class: "bg-red-500 hover:bg-red-700 "
                                    "text-white font-bold py-2 px-4 ml-2 rounded",
                                },
                                innerHTML="Delete",
                            ),
                        ],
                    ),
                ],
            ),
        ]
