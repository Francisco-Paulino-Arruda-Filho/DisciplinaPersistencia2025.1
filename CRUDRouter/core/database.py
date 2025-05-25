from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///mercado-livre.db", echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.commit()