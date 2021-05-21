from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,Float
from sqlalchemy import Column,MetaData,ForeignKey,Table
from sqlalchemy.dialects.mysql import (INTEGER,CHAR)
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:123456@localhost:3306/epc_data?charset=utf8",echo=True)
#engine=create_engine("mysql+pymysql://root:123456@localhost:3306/epc_data")
Base=declarative_base()
class MmeData(Base):
    __tablename__='mme_data'
    id=Column(Integer,primary_key=True)
    entity_name=Column(String(50))
    enb_num=Column(Integer)
    atta_2g_num=Column(Integer)
    atta_4g_num = Column(Integer)
    atta_success_ratio=Column(Float)
    date_time=Column(DateTime)

class SaegwData(Base):
    __tablename__='saegw_data'
    id=Column(Integer,primary_key=True)
    entity_name = Column(String(50))
    sgi_flow = Column(Float)
    session_2g_num = Column(Integer)
    session_4g_num = Column(Integer)
    date_time=Column(DateTime)

class FwData(Base):
    __tablename__='fw_data'
    id=Column(Integer,primary_key=True)
    entity_name = Column(String(50))
    session_num = Column(Integer)
    trunk1_in_flow = Column(Float)
    trunk2_in_flow = Column(Float)
    trunk3_in_flow = Column(Float)
    trunk4_in_flow = Column(Float)
    date_time = Column(DateTime)
#print('module is running')
Base.metadata.create_all(engine)

def get_mysql_session():
    DBsession=sessionmaker(bind=engine)
    session=DBsession()
    return session
if __name__=='__main__':
    session=get_mysql_session()
