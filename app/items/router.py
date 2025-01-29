from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.items.schemas import ItemsCreate, ItemsUpdate
from app.items.service import ItemsService
from app.kit.router import respond_to
from app.kit.sqlite import AsyncSession, get_async_db_session
from app.models import Items
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


@router.get(Paths.list_items, response_model=List[Items])
async def list_items(
    request: Request,
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Union[HTMLResponse, List[Items]]:
    data = await items_svc.list_items(db=db)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.get(Paths.new_item, response_model=None)
async def new_item() -> HTMLResponse:
    return await NewItemsPage().doc.render_html()


@router.get(Paths.show_item, response_model=Items)
async def show_item(
    request: Request,
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Union[HTMLResponse, Items]:
    data = await items_svc.get_item(db=db, item_name=item_name)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.show_item_page},
        },
    )


@router.post(Paths.create_item, response_model=Items)
async def create_item(
    request: Request,
    items_create: ItemsCreate = Body(
        ..., example=ItemsCreate.Config.json_schema_extra["example"]
    ),
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Union[HTMLResponse, Items]:
    if await items_svc.get_item(db=db, item_name=items_create.name):
        raise HTTPException(status_code=409, detail="Item already exists")
    data = await items_svc.create_item(db=db, items_create=items_create)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.put(Paths.update_item, response_model=Items)
async def update_item(
    request: Request,
    item_name: str,
    item_update: ItemsUpdate = Body(
        ..., example=ItemsUpdate.Config.json_schema_extra["example"]
    ),
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Union[HTMLResponse, Items]:
    item = await items_svc.get_item(db=db, item_name=item_name)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data = await items_svc.update_item(db=db, item=item, items_update=item_update)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": data},
            ResponseFormat.html: {"data": data, "page": items_svc.list_items_page},
        },
    )


@router.delete(Paths.delete_item, response_model=None)
async def delete_item(
    request: Request,
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Union[HTMLResponse, None]:
    if not await items_svc.get_item(db=db, item_name=item_name):
        raise HTTPException(status_code=204, detail="No Content")
    await items_svc.delete_item(db=db, item_name=item_name)
    return await respond_to(
        request,
        {
            ResponseFormat.json: {"data": {"message": f"deleted {item_name}"}},
            ResponseFormat.html: {"data": None, "page": items_svc.list_items_page},
        },
    )
