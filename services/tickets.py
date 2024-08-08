import os
from typing import Any, Dict, List

import dotenv
from jose import jwt
from asyncpg import Connection

import jinja2

from models.ticket import AddTicketModel

from fastapi.exceptions import HTTPException

dotenv.load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


async def get_tickets(
        connection: Connection,
        token: str
) -> str:
    tickets = await connection.fetchrow(
        """SELECT * FROM tickets WHERE hash = $1;""",
        token
    )

    await connection.execute(
        "UPDATE tickets SET scans = scans + 1 WHERE hash = $1;",
        token
    )

    if tickets is None:
        raise HTTPException(status_code=404, detail="Билет не найден")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/'),
        comment_start_string='{=',
        comment_end_string='=}',
    )
    template = env.get_template('result.html')

    html = template.render(
        scans=tickets['scans'],
        table_id=tickets['table_id'],
        sit_id=tickets['sit_id'],
        price=tickets['price'],
    )

    return html


async def decode_ticket(
        connection: Connection,
        ticket: AddTicketModel
) -> str:
    to_encode = {
        "table_id": ticket.table_id,
        "sit_id": ticket.sit_id,
        "price": ticket.price
    }
    encoded = jwt.encode(to_encode, JWT_SECRET_KEY, "HS256")

    existed_ticket = await connection.fetchrow(
        """SELECT * FROM tickets WHERE hash = $1;""",
        encoded
    )

    if existed_ticket is not None:
        return encoded

    await connection.execute(
        """INSERT INTO tickets (table_id, sit_id, price, hash)
        VALUES ($1, $2, $3, $4);""",
        ticket.table_id, ticket.sit_id, ticket.price, encoded
    )
    return encoded
