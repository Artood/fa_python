from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://fa_postgres:fa_postgres@fa_postgres:5432/fa_postgres")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    inn = Column(String, unique=True, nullable=False)
    contract_number = Column(String, nullable=True)
    contact_person = Column(String, nullable=True)
    external_prefix = Column(String, nullable=True)
    ip_dmz = Column(String, nullable=True)
    ip_inside = Column(String, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

class ClientCreate(BaseModel):
    name: str
    inn: str 
    contract_number: str | None = None
    contact_person: str | None = None
    external_prefix: str | None = None
    ip_dmz: str | None = None
    ip_inside: str | None = None

class ClientResponse(ClientCreate):
    id: int
    class Config:
        from_attributes = True

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/clients/", response_model=ClientResponse)
async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def read_client(client_id: int, db: AsyncSession = Depends(get_db)):
    client = await db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(client_id: int, client: ClientCreate, db: AsyncSession = Depends(get_db)):
    db_client = await db.get(Client, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client.model_dump().items():
        setattr(db_client, key, value)
    
    await db.commit()
    await db.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    db_client = await db.get(Client, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await db.delete(db_client)
    await db.commit()
    return {"message": "Client deleted successfully"}
