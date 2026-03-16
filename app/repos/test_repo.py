from sqlalchemy.orm import Session
from app.models.test import Test

def get_or_create_test(db: Session, message: str):
    test = db.query(Test).filter(Test.message == message).first()
    if not test:
        test = Test(message=message)
        db.add(test)
        db.commit()
        db.refresh(test)
    return test