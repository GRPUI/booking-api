from pydantic import BaseModel


class AddTicketModel(BaseModel):
    table_id: int
    sit_id: int
    price: int

