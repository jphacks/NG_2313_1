from pydantic import BaseModel


class AskQuestionResponse(BaseModel):
    answer: str
    status: str