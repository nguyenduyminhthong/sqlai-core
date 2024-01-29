from pydantic import BaseModel


class RelatedQuestion(BaseModel):
    sql: str
    question: str
    time_created: str | None = None


class RelatedDdl(BaseModel):
    ddl: str
    time_created: str | None = None


class RelatedDoc(BaseModel):
    doc: str
    time_created: str | None = None
