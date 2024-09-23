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

    existing_domain = db.query(Domain).filter(Domain.identifier == domain.identifier).first()

    if existing_domain:
           return{
                  "identifier" : existing_domain.identifier,
                  "key" : existing_domain.token,
                  "subdomain" : existing_domain.subdomain
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

@app.post("/update")
def update_subdomain(domain: DomainCreate, db: Session = Depends(get_db)):

    existing_domain = db.query(Domain).filter(Domain.identifier == domain.identifier).first()

    # identifier가 존재하지 않는 경우 에러 처리
    if not existing_domain:
        return {"error": "Identifier not found"}
    
    
    existing_domain.display_name = domain.display_name
    existing_domain.subdomain = domain.subdomain
    db.commit()
    db.refresh(existing_domain)

    return{
            "identifier" : existing_domain.identifier,
            "key" : existing_domain.token,
            "subdomain" : existing_domain.subdomain
    }

@app.post("/delete/{identifier}")
def delete_subdomain(identifier: str, db: Session = Depends(get_db)):
    domain_to_delete = db.query(Domain).where(Domain.identifier == identifier).first()
    
    if not domain_to_delete:
        return {"error" : "subdomain not found"}
    
    db.delete(domain_to_delete)
    db.commit()
       
    return {"message" : f"Subdomain `{domain_to_delete.subdomain}` deleted successfully"}
       

@app.get("/identifier/{identifier}")
def get_subdomain(identifier: str, db: Session = Depends(get_db)):
        return db.query(Domain).where(Domain.identifier == identifier).all()

@app.get("/subdomain/{subdomain}")
def exist_domain(subdomain: str, db: Session = Depends(get_db)):
        return db.query(Domain).where(Domain.subdomain == subdomain).count() > 0
