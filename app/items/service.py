from typing import Sequence

from sqlmodel import desc, select

from app.items.schemas import ItemsCreate, ItemsUpdate
from app.kit.html import Attr, Element, Tag
from app.kit.sqlite import AsyncSession
from app.models import Items
from app.pages.items import ListItemsPage, ShowItemPage


class ItemsService:
    async def list_items(self, db: AsyncSession) -> Sequence[Items]:
        results = await db.exec(select(Items).order_by(desc(Items.updated_at)))
        return results.all()

    async def create_item(self, db: AsyncSession, items_create: ItemsCreate) -> Items:
        item = Items(**items_create.model_dump())
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def get_item(self, db: AsyncSession, item_name: str) -> Items | None:
        item = await db.exec(select(Items).where(Items.name == item_name))
        return item.one_or_none()

    async def delete_item(self, db: AsyncSession, item_name: str) -> None:
        item = await self.get_item(db, item_name)
        if item:
            await db.delete(item)
            await db.commit()

    async def update_item(
        self, db: AsyncSession, item: Items, items_update: ItemsUpdate
    ) -> Items:
        for key, value in items_update.model_dump().items():
            setattr(item, key, value)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def show_item_page(self, data: Items) -> ShowItemPage:
        return ShowItemPage(data)

    async def list_items_page(
        self, data: Sequence[Items] | None | Items
    ) -> ListItemsPage:
        if data is None:
            data = []

        if data and isinstance(data, Items):
            data = [data]

        list_items_page = ListItemsPage()
        page_items = list_items_page.doc.body[0].children
        assert page_items is not None
        assert isinstance(data, list)

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
