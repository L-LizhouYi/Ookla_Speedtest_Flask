from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import pytz

# 创建数据库引擎
engine = create_engine('sqlite:///speedtest.db')
# 创建表格基类
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
    guid = Column(String, unique=True, default=str(uuid.uuid4()))
    # resultDate = Column(DateTime, default=datetime.utcnow)
    resultDate = Column(DateTime, default=datetime.now(cst))


class Speedtest:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def __del__(self):
        self.session.close()

    # 从数据库中获取服务器
    def get_servers(self):
        server_records = self.session.query(SpeedtestServer).limit(10).all()
        for server in server_records:
            yield {
                "id": server.id,
                "sponsor": server.sponsor,
                "name": server.name,
                "host": server.host,
                "url": server.url,
                "country": server.country,
                "cc": server.cc,
                "lat": server.lat,
                "lon": server.lon,
                "distance": server.distance,
                "preferred": server.preferred,
                "https_functional": server.https_functional,
                "force_ping_select": server.force_ping_select,
                "show": server.show,
                "internal": server.internal
            }

    # 通过id获取单个服务器信息
    def get_server_info(self, id):
        result = self.session.query(SpeedtestServer).filter_by(id=id).first()
        result = {
            "serverSponsor": result.sponsor,
            "serverName": result.name
        }
        return result

    # 添加测速记录
    def add_speedtest_log(self,data):
        # data = {
        #     "ispName": "39.87.54.3",
        #     "serverSponsor": "湖南联通5G（官方）",
        #     "serverName": "长沙",
        #     "serverId": 0,
        #     "jitter": 47.888888888888886,
        #     "latency": 36,
        #     "upload": 5699375,
        #     "download": 1319375,
        #     "guid": "0938c990-4d90-11ee-a138-3d1d9426b53e"
        # }

        speedtest_history = SpeedtestHistory(**data)
        self.session.add(speedtest_history)
        self.session.commit()

    # 获取测速记录
    def get_speedtest_log(self, guid):
        result = self.session.query(SpeedtestHistory).filter_by(guid=guid).first()
        result = {
            "ispName": result.ispName,
            "serverSponsor": result.serverSponsor,
            "serverName": result.serverName,
            "serverId": result.serverId,
            "jitter": result.jitter,
            "latency": result.latency,
            "upload": result.upload,
            "download": result.download,
            "guid": result.guid,
            "resultDate": result.resultDate.strftime('%Y-%m-%d %H:%M:%S')
        }
        return result


if __name__ == '__main__':
    # 创建表格
    Base.metadata.create_all(engine)

    # 添加Server服务器
    # server_info = SpeedtestServer(
    #     sponsor="Home (内网)",
    #     name="Esxi交换机",
    #     host="sp_home.eeho.cn:8080",
    #     url="http://sp_home.eeho.cn:8080/speedtest/upload.php",
    #     country="China",
    #     cc="CN",
    #     lat=0.0,
    #     lon=0.0,
    #     distance=40,
    #     preferred=0,
    #     https_functional=1,
    #     force_ping_select=1,
    #     show=1,
    #     internal=0
    # )
    #
    # # 添加记录到会话并提交更改
    # session.add(server_info)
    # session.commit()

