from pydantic import BaseModel
from typing import List


class ReceiptItem(BaseModel):
    item_name: str
    quantity: float
    unit_price: float
    amount: float


class Receipt(BaseModel):
    store_name: str
    date: str
    items: List[ReceiptItem]
    subtotal: float
    tax: float
    total: float