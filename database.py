# -*- coding: utf-8 -*-
"""
作用：
1、连接数据库
2、创建表

"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

#  sqlacodegen --tables taskthree "postgresql://postgres:postgres@202.120.167.50:5432/postgres" >tmp.py

host = '*****'
port = '5432'
username = 'postgres'
password = '******'
database = 'postgres'
dd = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)
# ?charset=utf8'

# 注意要设置charset，不然插入中文会报错
# 获取数据库引擎
engine = create_engine(dd)

Base = declarative_base(engine)

# 定义一个Taskthree类，数据表名为：待定

class Taskthree(Base):
    __tablename__ = 'taskthree'

    id = Column(Integer, primary_key=True, server_default=text("nextval('taskthree_id_seq'::regclass)"))
    description = Column(String)
    begintime = Column(Date, nullable=False)
    endtime = Column(Date, nullable=False)
    performer = Column(String, nullable=False)
    state = Column(String, nullable=False)
    title = Column(String, nullable=False)


# class User(Base):
#     __tablename__ = 'users'
#
#     nick_name = Column(String(10), primary_key=True)
#     user_name = Column(String(10), nullable=False)
#     passwd = Column(String(32), nullable=False)
#     phone = Column(String(11))
#     email = Column(String(20), nullable=False)

# 创建数据表，如果已经存在则忽略
Base.metadata.create_all()

# 获取数据库连接，提供给外部使用
conn = engine.connect()

'''
数据操作：
1、添加/更新数据
2、查询数据
3、删除数据
'''

# 创建与数据库的会话session，这里返回的是一个类class，不是实例
Session = sessionmaker(bind=engine)  # 绑定engine
session = Session()  # 初始化session实例


class UseData():
    # 1、添加/更新数据
    def insert_taskthree(self,data):
        result = Taskthree(performer=data[0], description=data[1], begintime=data[2], endtime=data[3], state=data[4], title=data[5])
        session.add(result)  # 提交数据
        session.commit()  # 提交，保存到数据库中，不写这句话，就不会保存到数据库的
        session.close()   #关闭会话

    #2.查询数据
    def select_taskthree(self):
        self.all = []       #建立一个空列表存放最后的数据
        selectList = session.query(Taskthree).all()       #查询所有的数据
        for i in selectList:        #循环存放结果，因为查询结果是一个对象
            person = [i.id, i.description, i.begintime, i.endtime, i.performer, i.state, i.title]
            self.all.append(person)
        return self.all        #返回list数据

    #3、条件查询数据
    def select_taskthree_sta(self,state):
        selectListsta = session.query(Taskthree).filter(Taskthree.state == state).first()     #条件查询
        selist = [selectListsta.performer, selectListsta.description, selectListsta.begintime, selectListsta.endtime, selectListsta.state, selectListsta.title]   #对象转化成列表
        return  selist   #返回list数据

    #4、数据更改
    def update_taskthree(self, datasql):
        update = session.query(Taskthree).filter_by(id = datasql[-1]).first()   #限制性查询语句，再更改数据
        update.performer = datasql[0]
        update.title = datasql[1]
        update.description = datasql[2]
        update.state = datasql[3]
        update.begintime = datasql[4]
        update.endtime = datasql[5]
        session.add(update)        #提交数据
        session.commit()          #提交事务

    # 5、数据删除
    def del_taskthree(self,id):
        session.query(Taskthree).filter(Taskthree.id == id).delete()       #删除掉那一行
        session.commit()         #事务提交

