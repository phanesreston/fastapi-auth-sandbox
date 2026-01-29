from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class Note(NoteCreate):
    id: int
    owner: str

