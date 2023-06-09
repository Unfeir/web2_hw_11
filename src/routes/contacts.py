from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactsResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get('/', response_model=List[ContactsResponse])
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.post('/', response_model=ContactsResponse, status_code=status.HTTP_201_CREATED)
async def add_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.add_contact(body, db)
    return contact


@router.get('/search', response_model=List[ContactsResponse])
async def search_contact(first_name: str = None, last_name: str = None, email: str = None,
                         db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contact(db, first_name, last_name, email)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get('/birthdays', response_model=List[ContactsResponse])
async def get_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_birthdays(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No birthdays in next week")
    return contacts


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.put('/{contact_id}', response_model=ContactsResponse)
async def change_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    contact = await repository_contacts.change_contact(contact_id, body, db)
    return contact


@router.get('/{contact_id}', response_model=ContactsResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
