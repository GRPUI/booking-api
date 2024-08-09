from asyncpg import Connection
from fastapi import APIRouter, Depends

from services import tickets

from fastapi.responses import HTMLResponse

from deps import DatabaseConnectionMarker
from models.ticket import AddTicketModel

router = APIRouter()


@router.get("/")
async def root(
    h: str,
    connection: Connection = Depends(DatabaseConnectionMarker)
) -> HTMLResponse:
    result = await tickets.get_tickets(connection, h)
    return HTMLResponse(content=result)


@router.post("/add/")
async def add_ticket(
    ticket: AddTicketModel,
    connection: Connection = Depends(DatabaseConnectionMarker)
) -> str:
    return await tickets.decode_ticket(connection, ticket)

