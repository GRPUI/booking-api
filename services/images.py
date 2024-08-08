import jinja2
from asyncpg import Connection

from fastapi.exceptions import HTTPException


async def get_ticket_image(
        connection: Connection,
        token: str
) -> str:
    ticket = await connection.fetchrow(
        """SELECT * FROM tickets WHERE hash = $1;""",
        token
    )
    if ticket is None:
        raise HTTPException(status_code=404, detail="Билет не найден")

    table_id, sit_id, price = ticket['table_id'], ticket['sit_id'], ticket['price']

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/'),
        comment_start_string='{=',
        comment_end_string='=}',
    )
    template = env.get_template('ticket.html')

    html = template.render(
        table_id=table_id,
        sit_id=sit_id,
        price=price,
        image=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data=ticket.pcost.tech/ticket/{token}"
    )

    return html
