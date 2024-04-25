from sqlalchemy import Column, Integer, String  # type: ignore
from .database import Base


class Bks(Base):
    __tablename__ = "bk"

    gnbkname = Column(String(10), primary_key=True, unique=True)
    code = Column(Integer)
    urlname = Column(String(50), unique=True)
    pinyin_start = Column(String(10), unique=False)
