from datetime import datetime

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import and_

from sqlalchemy.orm import Session

from models.transaction_subcategory import TransactionSubcategory, TransactionSubcategoryModel

def get_all_subcategories(engine):
    session = Session(engine)
    statement = select(TransactionSubcategory).where(TransactionSubcategory.logical_delete == False)
    result = session.execute(statement)
    categories = []
    for row in result:
        categories.append(TransactionSubcategoryModel(
            id=row[0].id,
            name=row[0].name,
            transaction_category_id=row[0].transaction_category_id
        ))
    
    session.close()
    return categories

def get_subcategories(engine, category_id):
    statement = select(
        TransactionSubcategory
    ).where(
        and_(
            TransactionSubcategory.transaction_category_id == category_id,
            TransactionSubcategory.logical_delete == False
        )
    )
    session = Session(engine)
    result = session.execute(statement)
    categories = []
    for row in result:
        categories.append(TransactionSubcategoryModel(
            id=row[0].id,
            name=row[0].name,
            transaction_category_id=row[0].transaction_category_id
        ))
    
    session.close()
    return categories