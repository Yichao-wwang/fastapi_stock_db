from datetime import date
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List


def get_books_with_limit_offset(db: Session, offset: int, limit: int) -> List[models.Bks]:
    return db.query(models.Bks).offset(offset).limit(limit).all()


def get_gnbk_by(db: Session, bookname: str):
    query1 = db.query(models.Bks).filter(models.Bks.gnbkname.like(f"%{bookname}%"))
    query2 = db.query(models.Bks).filter(models.Bks.pinyin_start.like(f"%{bookname}%"))
    query3 = db.query(models.Bks).filter(models.Bks.code.like(f"%{bookname}%"))
    # 使用 JOIN 来连接两个查询结果
    # 将所有非空查询结果连接起来
    combined_query = None
    if query1 != []:
        combined_query = query1
    if query2 != []:
        if combined_query is None:
            combined_query = query2
        else:
            combined_query = combined_query.union(query2)
    if query3 != []:
        if combined_query is None:
            combined_query = query3
        else:
            if query1 != [] and query2 != []:
                combined_query = combined_query.union(query3)

    if combined_query is not None:
        return combined_query.all()
    else:
        return []

    return combined_query.all()


def delete_book_by_code(db: Session, code: int):
    db_book = db.query(models.Bks).filter(models.Bks.code == code).one_or_none()
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return True


def create_book(db: Session, book: schemas.BKs):
    curBook = models.Bks(
        gnbkname=book.gnbkname,
        code=book.code,
        urlname=book.urlname,
        pinyin_start=book.pinyin_start
    )
    db.add(curBook)
    db.commit()
    db.refresh(curBook)
    return curBook
