from sqlmodel import select
from app.controllers.exceptions import NotFoundError
from app.controllers.utils import rollback_and_raise

def get_all(session, model, operation):
    try: 
        return session.exec(select(model)).all()
    except Exception as exc: 
        rollback_and_raise(session, exc, operation)

def get_one(session, model, item_id, operation, label):
    try:
        item = session.get(model, item_id)
        if item is None: 
            raise NotFoundError(f"{label} с указанным ID не найден")
        return item
    except NotFoundError: 
        raise
    except Exception as exc: 
        rollback_and_raise(session, exc, operation)

def create_one(session, model, data, operation):
    try:
        item = model(**data.model_dump(exclude_unset=True, exclude_none=True))
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as exc: 
        rollback_and_raise(session, exc, operation)

def update_one(session, model, item_id, data, operation, label):
    try:
        item = session.get(model, item_id)
        if item is None: 
            raise NotFoundError(f"{label} с указанным ID не найден")
        for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(item, key, value)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except NotFoundError:
        raise
    except Exception as exc:
        rollback_and_raise(session, exc, operation)

def delete_one(session, model, item_id, operation, label):
    try:
        item = session.get(model, item_id)
        if item is None:
            raise NotFoundError(f"{label} с указанным ID не найден")
        session.delete(item)
        session.commit()
    except NotFoundError:
        raise
    except Exception as exc:
        rollback_and_raise(session, exc, operation)
