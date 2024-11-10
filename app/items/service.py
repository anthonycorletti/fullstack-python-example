from typing import List

from app.database import db
from app.items.schemas import ItemCreate, ItemUpdate
from app.kit.html import Attr, Element, Tag
from app.models import Item
from app.pages.items import ListItemsPage, ShowItemPage


class ItemsService:
    async def list_items(self) -> List[Item]:
        return list(db.values())

    async def create_item(self, item_create: ItemCreate) -> Item:
        data = Item(**item_create.model_dump())
        if data.name in db:
            db[data.name].count += data.count
        else:
            db[data.name] = data
        return data

    async def list_items_page(self, data: List[Item] | Item | None) -> ListItemsPage:
        if data is None or isinstance(data, Item):
            data = await self.list_items()

        list_items_page = ListItemsPage()
        page_items = list_items_page.doc.body[0].children
        assert page_items is not None

        if len(data) == 0:
            page_items.append(
                Element(
                    tag=Tag.p,
                    children=[
                        "There are no items.",
                    ],
                )
            )
        else:
            page_items.append(
                Element(
                    tag=Tag.ul,
                    children=[
                        Element(
                            tag=Tag.li,
                            children=[
                                f"{item.name} - {item.count} - {item.description}",
                                Element(
                                    tag=Tag.a,
                                    attrs={
                                        "href": f"/items/{item.name}",
                                        Attr._class: "underline font-bold"
                                        " hover:text-blue-500 pl-2",
                                    },
                                    children=["edit"],
                                ),
                                Element(
                                    tag=Tag.span,
                                    attrs={
                                        Attr._class: "underline font-bold"
                                        " hover:text-red-500 pl-2",
                                        Attr.hx_delete: f"/items/{item.name}",
                                        Attr.hx_confirm: "Are you sure?",
                                        Attr.hx_swap: "outerHTML",
                                        Attr.hx_target: "#listItemTarget",
                                        Attr.hx_replace_url: "/items",
                                    },
                                    children=["delete"],
                                ),
                            ],
                        )
                        for item in data
                    ],
                )
            )
        return list_items_page

    async def get_item(self, item_name: str) -> Item | None:
        if item_name in db:
            return db[item_name]
        else:
            return None

    async def delete_item(self, item_name: str) -> None:
        db.pop(item_name)

    async def update_item(self, item: Item, item_update: ItemUpdate) -> Item:
        if item_update.name != item.name:
            db.pop(item.name)
        updated_dump = item.model_dump() | item_update.model_dump()
        updated_item = Item(**updated_dump)
        db[updated_dump["name"]] = updated_item
        return updated_item

    async def show_item_page(self, data: Item) -> ShowItemPage:
        return ShowItemPage(data)
