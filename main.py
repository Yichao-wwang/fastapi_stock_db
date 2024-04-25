from sqlalchemy.orm import Session  # type: ignore
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 设定数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates1 = Jinja2Templates(directory="sql_app/templates")


@app.get("/boo", response_class=HTMLResponse)
def show_all_books(request: Request, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_books = crud.get_books_with_limit_offset(db, offset=offset, limit=limit)
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found")
    return templates1.TemplateResponse("index.html", {"request": request, "books": db_books})


@app.get("/load_more_books")
def load_more_books(offset: int, limit: int, db: Session = Depends(get_db)):
    db_books = crud.get_books_with_limit_offset(db, offset=offset, limit=limit)
    if not db_books:
        return JSONResponse(content=[], status_code=200)
    return db_books


@app.get("/stock/", response_model=list[schemas.BKs])
def get_pinyin(name: str, db: Session = Depends(get_db)):
    db_books = crud.get_gnbk_by(db, bookname=name)
    if not db_books:
        raise HTTPException(status_code=400, detail="THS no this gnbk")
    return db_books


@app.post("/delete/{bookid}")
def delete_book(code: int, db: Session = Depends(get_db)):
    return crud.delete_book_by_code(db, code=code)


@app.post("/books/", response_model=schemas.BKs)
def create_book(book: schemas.BKs, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book=book)
    if db_book:
        raise HTTPException(status_code=400, detail="该书籍已经存在。")
    return crud.create_book(db=db, book=book)
