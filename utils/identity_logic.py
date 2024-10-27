from datetime import datetime

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from sqlalchemy.orm import Session

from models.identity import Identity, IdentityModel
from models.identity_type import IdentityTypeModel

def create_identity(identity: IdentityModel, engine):
    session = Session(engine)
    result = session.execute(
        insert(Identity),
        [
            {
                "name": identity.name,
                "type_id": identity.type_id,
                "updated_at": datetime.now(),
                "logical_delete": False
            }
        ]
    )
    session.commit()
    session.close()
    return 1

def get_all_identities(engine):
    session = Session(engine)
    result = session.execute(
        select(Identity)
        .where(Identity.logical_delete == False)
    )
    results = []
    for row in result:
        results.append(IdentityModel(
            id=row[0].id,
            name=row[0].name,
            type_id=row[0].type.id,
            type=IdentityTypeModel(
                id=row[0].type.id,
                name=row[0].type.name
            )
        ))
    session.close()
    return results

def get_identity(id, engine):
    session = Session(engine)
    row = session.execute(
        select(Identity)
        .where(Identity.id == id)
        .where(Identity.logical_delete == False)
    ).first()
    if (row != None):
        result = IdentityModel(
            id=row[0].id,
            name=row[0].name,
            type_id=row[0].type.id,
            type=IdentityTypeModel(
                id=row[0].type.id,
                name=row[0].type.name
            )
        )
        return result
    session.close()

def update_identity(identity: IdentityModel, engine):
    session = Session(engine)
    result = session.execute(
        update(Identity)
        .where(Identity.id == identity.id)
        .values(
            name=identity.name,
            type_id=identity.type_id,
            updated_at=datetime.now()
        )
    )
    session.commit()
    session.close()
    return result.rowcount

def revive_identity(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Identity)
        .where(Identity.id == id)
        .values(updated_at=datetime.now(), logical_delete = False)
    )
    session.commit()
    session.close()
    return results.rowcount

def delete_identity(id, engine):
    session = Session(engine)
    results = session.execute(
        update(Identity)
        .where(Identity.id == id)
        .values(updated_at=datetime.now(), logical_delete = True)
    )
    session.commit()
    session.close()
    return results.rowcount