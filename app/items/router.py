from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.items.schemas import ItemCreate, ItemUpdate
from app.items.service import ItemsService
from app.kit.router import respond_to
from app.models import Item
from app.pages.items import NewItemsPage
from app.settings import ResponseFormat

router = APIRouter(tags=["items"])


class Paths:
    list_items = "/items"
    create_item = "/items"
    new_item = "/items/new"
    show_item = "/items/{item_name}"
    update_item = "/items/{item_name}"
    delete_item = "/items/{item_name}"


@router.get(
    Paths.list_items,
    response_model=List[Item],
)
async def list_items(
    request: Request,
    items_svc: ItemsService = Depends(ItemsService),
) -> Union[HTMLResponse, List[Item]]:
    data = await items_svc.list_items()
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.get(
    Paths.new_item,
    response_model=None,
)
async def new_item() -> HTMLResponse:
    return await NewItemsPage().doc.render_html()


@router.get(
    Paths.show_item,
    response_model=Item,
)
async def show_item(
    request: Request,
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
) -> Union[HTMLResponse, Item]:
    data = await items_svc.get_item(item_name=item_name)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.show_item_page},
        },
    )


@router.post(
    Paths.create_item,
    response_model=Item,
)
async def create_item(
    request: Request,
    item_create: ItemCreate = Body(
        ...,
        example=ItemCreate.Config.json_schema_extra["example"],
    ),
    items_svc: ItemsService = Depends(ItemsService),
) -> Union[HTMLResponse, Item]:
    data = await items_svc.create_item(item_create=item_create)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.put(
    Paths.update_item,
    response_model=Item,
)
async def update_item(
    request: Request,
    item_name: str,
    item_update: ItemUpdate = Body(
        ...,
        example=ItemUpdate.Config.json_schema_extra["example"],
    ),
    items_svc: ItemsService = Depends(ItemsService),
) -> Union[HTMLResponse, Item]:
    item = await items_svc.get_item(item_name=item_name)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data = await items_svc.update_item(item=item, item_update=item_update)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.delete(
    Paths.delete_item,
    response_model=None,
)
async def delete_item(
    request: Request,
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
) -> Union[HTMLResponse, None]:
    if not await items_svc.get_item(item_name=item_name):
        raise HTTPException(status_code=204, detail="No Content")
    await items_svc.delete_item(item_name=item_name)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": {"message": f"deleted {item_name}"}},
            ResponseFormat.html: {"data": None, "page": items_svc.list_items_page},
        },
    )
