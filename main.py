# This is a sample Python script.
import threading
import time
import uuid
from util import config
from werkzeug.utils import secure_filename

from util import FormatUtil, Sessions

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request
from db.dbData import DBData

app = Flask(__name__)
dbData = DBData()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press Ctrl+F8 to toggle the breakpoint.


@app.route("/api/login", methods=['POST'])
def login():
    datas = request.get_json()
    if datas is not None:
        res = dbData.login(datas)
        if len(res) > 0:
            res[0]['login_pwd'] = ""
            Sessions.setUser(res[0])
        return res
    return [False]


@app.route("/api/addPerson", methods=['POST'])
def addPerson():
    datas = request.get_json()
    datas['idkey'] = str(uuid.uuid4())
    if datas is not None:
        saveData = [(
            datas['idkey'],
            datas['name'],
            datas['login_name'],
            datas['login_pwd'],
            datas['gender'],
            datas['remark'],
            datas['phone'],
        )]
        res = dbData.addPerson(saveData)
        return [res]
    return [False]


@app.route("/api/addFamily", methods=['POST'])
def addFamily():
    datas = request.get_json()
    datas['idkey'] = str(uuid.uuid4())
    if datas is not None:
        datas['create_time'] = FormatUtil.getCurrentTimeStamp()
        datas['idkey'] = str(uuid.uuid4())
        saveData = [(
            datas['idkey'],
            datas['family_name'],
            datas['person_m_idkey'],
            datas['person_f_idkey'],
            datas['create_person'],
            datas['create_time'],
            datas['remark'],
        )]
        res = dbData.addFamily(saveData)
        return [res]
    return [False]


@app.route("/api/getPerson", methods=['POST'])
def getPerson():
    res = dbData.getPersons()
    datas = []
    for item in res:
        datas.append({'idkey': item[0], 'name': item[1], 'gender': item[2]})
    return datas


@app.route("/api/getFamilyInfoAllByFamilyId", methods=['POST'])
def getFamilyInfoAllByFamilyId():
    datas_r = []
    datas = request.get_json()
    personId = datas['idkey']
    if personId is not None:
        datas_r = dbData.selectFamilyPersonsByFamilyIdKey(personId)
    return datas_r


# @app.route('/api/uploadFile', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['the_file']
#         file.save(f"/var/www/uploads/{secure_filename(file.filename)}")


@app.route("/api/test", methods=['POST', 'get'])
def apiTest():
    return "ok"


@app.route("/api/getResource", methods=['POST', 'get'])
def getResource():
    datas_r = []
    datas = request.get_json()
    print(datas)
    datas_r = dbData.getResource(datas)
    return datas_r


@app.route("/api/addRecord", methods=['POST'])
def addRecord():
    datas = request.get_json()
    # idkey,belong_type, belong_idkey, level, datetime,subject, remark, base_image_id, type,create_person,create_time, content)
    if datas is not None:
        datas['create_time'] = FormatUtil.getCurrentTimeStamp()
        datas['idkey'] = str(uuid.uuid4())
        saveData = [(
            datas['idkey'],  # idkey
            datas['belongType'],
            datas['belongIdkey'],
            datas['level'],
            datas['create_time'],
            datas['name'],
            datas['remark'],
            "",
            5,
            datas['create_person'],
            datas['create_time'],
            datas['content']
        )]
        res = dbData.addRecord(saveData)
        if res is True:
            return {"code": 1, "msg": "保存成功", "idkey": datas['idkey']}
        else:
            return {"code": 0, "msg": "保存失败！"}
    else:
        return {"code": 0, "msg": "提交内容为空！"}


@app.route("/api/selectRecord", methods=['POST'])
def selectRecord():
    datas = request.get_json()
    return dbData.getRecord(datas['belongIdkey'])


@app.route("/api/updateRecord", methods=['POST'])
def updateRecord():
    datas = request.get_json()
    if datas is not None:
        saveData = (
            datas['idkey'],  # idkey
            datas['name'],
            datas['remark'],
            datas['content']
        )
        res = dbData.updateRecord(saveData)
        if res is True:
            return {"code": 1, "msg": "操作成功！"}
        else:
            return {"code": 0, "msg": "操作失败！"}
    return {"code": 0, "msg": "提交数据为空！"}


@app.route('/api/upload', methods=['POST'])
def upload():
    datas = request.form.to_dict()
    print(datas)
    files = request.files['file']  # 'file'为HTML表单中input标签的名称
    dirName = f'{config.file_root_path}{FormatUtil.makeDirNameByDate()}'
    # print(files)
    FormatUtil.create_folder_if_not_exists(dirName)
    # for file in files:
    filename = files.filename.split(".")
    fileExt = filename[len(filename) - 1]
    fileSaveName = f'{uuid.uuid4()}.{fileExt}'
    # print(fileSaveName)
    filePath = f'{dirName}/{fileSaveName}'
    files.save(filePath)
    datas['resource_path'] = filePath
    datas['idkey'] = str(uuid.uuid4())
    dbData.addResource([(datas['idkey'], datas['upload_person'], datas['resource_name'], datas['resource_type'],
                         datas['resource_path'], datas['create_person'], datas['create_time'], datas['remark'])])
    return {"code": 1, "msg": "文件上传成功！"}


def startServer():
    app.debug = False
    app.run(port=8066, host="localhost", debug=False)  # 10.64.78.149 localhost


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('============================')
    print_hi('=Family Backend Starting...=')
    print_hi('============================')
    # t1 = threading.Thread(target=startServer)
    # t1.start()
    startServer()
    # FormatUtil.startNginx()
    # FormatUtil.openBrowser()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
