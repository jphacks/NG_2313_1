from pydantic import BaseModel
from typing import List

class StorePDF(BaseModel):
    pdf

class AskAgent(BaseModel):
    db_name: str
    message: str