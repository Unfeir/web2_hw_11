from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip, limit, db: Session):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


async def get_contact(contact_id, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    return contact


async def search_contact(db, first_name=None, last_name=None, email=None):
    print(f'{first_name=}, {last_name=}, {email=}')
    contacts = None
    if first_name and last_name:
        contacts = db.query(Contact).filter(Contact.first_name == first_name, Contact.last_name == last_name).all()
    if first_name:
        contacts = db.query(Contact).filter(Contact.first_name == first_name).all()
    if email:
        contacts = db.query(Contact).filter(Contact.email == email).all()

    return contacts


async def add_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def change_contact(contact_id, body, db: Session):
    contact = await get_contact(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.birthday = body.birthday
        contact.email = body.email
        contact.address = body.address
        db.commit()
    return contact


async def remove_contact(contact_id, db: Session):
    contact = await get_contact(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthdays(db: Session):
    today = date.today()
    delta = timedelta(days=7)
    all_contacts = db.query(Contact).all()
    contacts = []
    for contact in all_contacts:
        if contact.birthday.replace(year=today.year) >= today and contact.birthday.replace(
                year=today.year) <= today + delta:
            contacts.append(contact)
    return contacts
