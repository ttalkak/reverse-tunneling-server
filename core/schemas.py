from pydantic import BaseModel

class DomainCreate(BaseModel):
    identifier: str
    display_name: str
    subdomain: str