from typing import Union

from fastapi import FastAPI, Depends

from uuid import uuid4
from sqlalchemy.orm import Session
from core.base import get_db
from core.models import Domain
from core.schemas import DomainCreate
from sqlalchemy import select

app = FastAPI()

@app.post("/create")
def create_subdomain(domain: DomainCreate, db: Session = Depends(get_db)):

    existing_domain = db.query(Domain).filter(Domain.subdomain == domain.subdomain).first()

    if existing_domain:
           return{
                  "identifier" : existing_domain.identifier,
                  "key" : existing_domain.token,
                  "sudomain" : existing_domain.subdomain
           }
    
    key = str(uuid4()).replace("-", "")
    
    create = Domain(
        identifier=domain.identifier, 
        display_name=domain.display_name,
        token=key,
        subdomain=domain.subdomain
    )
    db.add(create)
    db.commit()
    db.refresh(create)
    return {
        "identifier": domain.identifier,
        "key": key,
        "subdomain": domain.subdomain
    }

@app.get("/identifier/{identifier}")
def get_subdomain(identifier: str, db: Session = Depends(get_db)):
        return db.query(Domain).where(Domain.identifier == identifier).all()

@app.get("/subdomain/{subdomain}")
def exist_domain(subdomain: str, db: Session = Depends(get_db)):
        return db.query(Domain).where(Domain.subdomain == subdomain).count() > 0