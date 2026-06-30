from sqlalchemy import Column,Integer,String,DateTime,Text
from datetime import datetime
from app.database import Base

class Report(Base):
    __tablename__="reports"
    id=Column(Integer,primary_key=True,index=True)
    report_id=Column(String(64),unique=True,index=True)
    provider=Column(String(50))
    filename=Column(String(255))
    status=Column(String(50),default="completed")
    created_at=Column(DateTime,default=datetime.utcnow)
    content=Column(Text)
