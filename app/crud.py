from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Contact
from .schemas import ContactCreate, ContactUpdate
from sqlalchemy import or_
from datetime import datetime, timedelta


async def create_contact(db: AsyncSession, contact: ContactCreate, user_id: int):
    db_contact = Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def get_contacts(db: AsyncSession, current_user):
    result = await db.execute(select(Contact).where(Contact.user_id == current_user.id))
    return result.scalars().all()

async def get_contact_by_id(db: AsyncSession, contact_id: int, user_id: int):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id))
    return result.scalar_one_or_none()

async def update_contact(db: AsyncSession, contact_id: int, user_id: int, contact_data: ContactUpdate):
    contact = await get_contact_by_id(db, contact_id, user_id)
    if not contact:
        return None  

    for key, value in contact_data.dict(exclude_unset=True).items():
        setattr(contact, key, value)

    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(db: AsyncSession, contact_id: int, user_id: int):
    contact = await get_contact_by_id(db, contact_id, user_id)
    if not contact:
        return False  

    await db.delete(contact)
    await db.commit()
    return True

async def search_contacts(db: AsyncSession, query: str):
    result = await db.execute(
        select(Contact).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
    )
    return result.scalars().all()

async def get_upcoming_birthdays(db: AsyncSession):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    result = await db.execute(
        select(Contact).where(
            Contact.birthday >= today,
            Contact.birthday <= next_week
        )
    )
    return result.scalars().all()