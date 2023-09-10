from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import pytz

engine = create_engine('sqlite:///speedtest.db')
Base = declarative_base()
cst = pytz.timezone('Asia/Shanghai')

# 定义数据模型类
class SpeedtestServer(Base):
    __tablename__ = 'speedtest_servers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sponsor = Column(String)
    name = Column(String)
    host = Column(String)
    url = Column(String)
    country = Column(String)
    cc = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    distance = Column(Integer)
    preferred = Column(Integer)
    https_functional = Column(Integer)
    force_ping_select = Column(Integer)
    show = Column(Integer)
    internal = Column(Integer)

class SpeedtestHistory(Base):
    __tablename__ = 'speedtest_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ispName = Column(String)
    serverSponsor = Column(String)
    serverName = Column(String)
    serverId = Column(Integer)
    jitter = Column(Float)
    latency = Column(Integer)
    upload = Column(Integer)
    download = Column(Integer)
    guid = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    resultDate = Column(DateTime, default=lambda: datetime.now(cst))


if __name__ == '__main__':
    # 创建表格
    Base.metadata.create_all(engine)