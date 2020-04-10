import psycopg2,sys
from flask import Flask, jsonify, request
from flask_cors import CORS
sys.path.append('../service')
# from datae basimport 
from database import UseData
U = UseData()


app = Flask(__name__)
CORS(app)

# conn = psycopg2.connect(
#         database="postgres", user="postgres", password="*****", host="*****", port="5432")


@app.route('/rest/anon/tasks',methods=['POST'])
def create():
    # cur = conn.cursor()
    data = request.get_json()
    # cur.execute("insert into taskthree(performer, description, begintime, endtime, state, title) values(%s,%s,%s,%s,%s,%s)",
    #          (data['performer'], data['description'], data['begintime'], data['endtime'], data['state'], data['title']))   #数据写入
    # conn.commit()
    data_sql = [data['performer'], data['description'], data['begintime'], data['endtime'], data['state'], data['title']]
    U.insert_taskthree(data_sql)
    return "1"


@app.route('/rest/anon/tasks',methods=['GET'])
def read():
    # cur = conn.cursor()
    # cur.execute(
    #     "select * from taskthree")   #数据库查询
    # rows = cur.fetchall()
    rows = U.select_taskthree()
    l = []
    for row in rows:
        print(row)
        dic= {'id': str(row[0]),'description': str(row[1]),'begintime':str(row[2]),'endtime':str(row[3]),'performer':str(row[4]),'state':str(row[5]),'title':str(row[6])}
        l.append(dic)
    return jsonify(l)


@app.route('/rest/anon/tasks/<string:state>',methods=['GET'])
def read_state(state):
    # cur = conn.cursor()
    # cur.execute(
    #     "select * from taskthree where state="+state)   #数据库查询
    # rows = cur.fetchall()
    rows = U.select_taskthree_sta(state)
    l = []
    for row in rows:
        # print(row)
        dic= {'id': str(row[0]),'description': str(row[1]),'begintime':str(row[2]),'endtime':str(row[3]),'performer':str(row[4]),'state':str(row[5]),'title':str(row[6])}
        l.append(dic)
    return jsonify(l)
#  select * from taskthree where begintime >=  and endtime < '2015-08-15';



@app.route('/rest/anon/tasks/<string:id>', methods=['PUT'])
def update(id):
    # cur = conn.cursor()
    data = request.get_json()
    data_sql = [data['performer'],data['title'],data['description'],data['state'],data['begintime'],data['endtime'],id]
    # cur.execute("UPDATE taskthree SET performer = '{}', title = '{}', description = '{}', state = '{}', begintime = '{}', endtime = '{}'  WHERE id = {}"
    #     .format(data['performer'],data['title'],data['description'],data['state'],data['begintime'],data['endtime'], id))      #数据库更改

    # conn.commit()
    U.update_taskthree(data_sql)

    return "1"


@app.route('/rest/anon/tasks/<string:id>', methods=['DELETE'])
def delete(id):
    # cur = conn.cursor()
    # cur.execute("DELETE from taskthree where id="+ id)    #数据库删除
    # conn.commit()
    U.del_taskthree(id)
    return "1"


if __name__ == '__main__':
    app.run()
