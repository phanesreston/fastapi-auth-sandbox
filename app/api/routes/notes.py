from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.notes import NoteCreate, Note

router = APIRouter(prefix="/notes", tags=["notes"])


NOTES: list[Note] = []
NEXT_ID = 1


@router.post("", response_model=Note)
def create_note(payload: NoteCreate, user=Depends(get_current_user)):
    global NEXT_ID

    note = Note(
        id=NEXT_ID,
        title=payload.title,
        content=payload.content,
        owner=user["username"],
    )
    NOTES.append(note)
    NEXT_ID += 1
    return note


@router.get("", response_model=list[Note])
def list_my_notes(user=Depends(get_current_user)):
    return [n for n in NOTES if n.owner == user["username"]]


@router.get("/{note_id}", response_model=Note)
def get_note(note_id: int, user=Depends(get_current_user)):
    for n in NOTES:
        if n.id == note_id:
            # owner or admin can view
            if n.owner != user["username"] and user["role"] != "admin":
                raise HTTPException(status_code=403, detail="Not allowed")
            return n
    raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}")
def delete_note(note_id: int, user=Depends(get_current_user)):
    for i, n in enumerate(NOTES):
        if n.id == note_id:
            # only owner can delete
            if n.owner != user["username"]:
                raise HTTPException(status_code=403, detail="Not allowed")
            NOTES.pop(i)
            return {"status": "deleted", "id": note_id}
    raise HTTPException(status_code=404, detail="Note not found")


@router.get("/admin/all", response_model=list[Note], tags=["admin"])
def list_all_notes(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return NOTES

