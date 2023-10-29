from pydantic import BaseModel
from typing import List

class StorePDF(BaseModel):
    pdf: str

class AskAgent(BaseModel):
    message: str