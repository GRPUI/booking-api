from asyncpg import Connection
from fastapi import APIRouter, Depends

from fastapi.responses import HTMLResponse

from services import images

from deps import DatabaseConnectionMarker

router = APIRouter()


@router.get("/{h}")
async def root(
    h: str,
    connection: Connection = Depends(DatabaseConnectionMarker)
):
    result = await images.get_ticket_image(connection, h)
    return HTMLResponse(content=result)