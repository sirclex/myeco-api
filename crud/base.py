from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        return db.query(self.model).get(model_id)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_multi_by(self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs) -> List[ModelType]:
        query = db.query(self.model)
        for attr, value in kwargs.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, attr).in_(value))
            else:
                query = query.filter(getattr(self.model, attr) == value)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_multi(self, db: Session, *, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db_objs.append(db_obj)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_none=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_multi(self, db: Session, *, objs_in: List[Union[UpdateSchemaType, Dict[str, Any]]]) -> List[ModelType]:
        db_objs = []
        for obj_in in objs_in:
            obj_data = jsonable_encoder(obj_in)
            db_obj = db.query(self.model).get(obj_data['id'])
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_none=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db_objs.append(db_obj)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs
    
    def delete(self, db: Session, *, model_id: int) -> ModelType:
        obj = db.query(self.model).get(model_id)
        db.delete(obj)
        db.commit()
        return obj