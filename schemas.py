from pydantic import BaseModel

class BksBase(BaseModel):
    gnbkname : str
    code :int
    urlname:str
    pinyin_start:str
class BKs(BksBase):
    class Config:
        from_attributes = True
