from sqlalchemy.orm import Session
from app.models import Report

def create_report(db:Session,**kwargs):
    obj=Report(**kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_report(db:Session,report_id:str):
    return db.query(Report).filter(Report.report_id==report_id).first()

def list_reports(db:Session):
    return db.query(Report).all()

def delete_report(db:Session,report_id:str):
    obj=get_report(db,report_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
