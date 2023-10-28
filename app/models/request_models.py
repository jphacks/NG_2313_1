from pydantic import BaseModel


class QA_pdf(BaseModel):
    collection_name: str
    pdf: str

class QA(BaseModel):
    collection_name: str
    question: str