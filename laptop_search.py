import pandas as pd
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session


def sanitize(string: str):
    return string.replace("[,", "").replace(",]", "")


Base = declarative_base()


class Processor(Base):
    __tablename__ = "processor"
    processor_id = Column(Integer, primary_key=True)
    series = Column(String(100))
    model = Column(String(100))
    frequency = Column(String(10))


class Laptop(Base):
    __tablename__ = "laptop"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    model = Column(String(100))
    producentKey = Column(String(30))
    screenSize = Column(String(10))

    processor_id = Column(Integer, ForeignKey("processor.processor_id"))
    processor = relationship("Processor")


from sqlalchemy import create_engine

engine = create_engine("sqlite:///file.db")

Base.metadata.create_all(engine)
df = pd.read_csv("prefilter-output-filtered.txt", encoding="1251", delimiter="\t")

with Session(bind=engine) as session:
    print((df.groupby("Model procesora").first()))
    for index, row in (df.groupby("Model procesora").first()).iterrows():
        proc = Processor()
        print(row)
        proc.model = sanitize(row.key)
        proc.series = sanitize(row["Seria procesora"])
        proc.frequency = sanitize(row["Taktowanie bazowe procesora"])
        session.add(proc)
    session.commit()
