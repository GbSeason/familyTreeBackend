import sqlite3
import uuid

from util.config import file_root_path


class DBData:
    __dbName = "family.db"
    # __table_create_log_info = '''create table if not exists log_info (
    #                     id_key   text   not null,
    #                     test_id    VARCHAR(50),
    #                     name    text,
    #                     label    text,
    #                     total    integer,
    #                     pass    integer,
    #                     fail    integer,
    #                     skip    integer,
    #                     start_time VARCHAR(50),
    #                     end_time VARCHAR(50),
    #                     elapsed    VARCHAR(50),
    #                     status  VARCHAR(50),
    #                     type    VARCHAR(50),
    #                     save_time VARCHAR(50),
    #                     file_id VARCHAR(50),
    #                     file_path VARCHAR(500) )'''
    # __table_create_log_info_detail = '''create table if not exists log_info_detail (
    #                         id_key   text   not null,
    #                         test_id    VARCHAR(50),
    #                         log_detail  text)'''
    # __table_create_rt_vkms = '''create table if not exists rt_vkms (
    #                         id_key   VARCHAR(50)   not null,
    #                         target_name    VARCHAR(50),--测试目标名称LAVTDMER6PA00000
    #                         target_vkms    integer,--状态 success
    #                         target_rat  VARCHAR(20),---信号类型let 3g 4g 5g
    #                         target_r_p integer,--rp状态 1:true 0:false
    #                         target_connect integer,--connect状态 1:true 0:false
    #                         received_time    VARCHAR(50),--接收时间
    #                         log_file_id VARCHAR(50) --日志文件标识
    #                         )'''
    # __table_create_rt_apn_speed = '''create table if not exists rt_vkms_speed (
    #                             id_key   text   not null,
    #                             target_id_key    text,--测试目标存储的标识
    #                             received_time    text,--接收时间
    #                             apn_1_speed     text,--传输速度
    #                             apn_2_speed     text --传输速度
    #                             )'''
    # __table_create_settings = '''create table if not exists settings_info (
    #                                 info_name    text,--名称
    #                                 info_value    text--值
    #                             )'''

    # ===============================
    # 成员表
    __table_create_person_info = '''create table if not exists person_info (
                                    idkey varchar(100) PRIMARY KEY, --主键
                                    family_idkey varchar(100), --所属家庭主键
                                    name    varchar(100),--姓名
                                    petname    varchar(100),--小名
                                    enname    varchar(100),--英文名
                                    login_name varchar(50),--登录名
                                    login_pwd varchar(50),--登录密码
                                    gender   varchar(10),--性别
                                    birthday TIMESTAMP,--出生日期
                                    idcard varchar(100),--身份证号
                                    nation varchar(100),--民族
                                    native_place varchar(100),--籍贯
                                    head_img text,--头像资源idkey
                                    remark text,--简介
                                    phone varchar(20),--电话
                                    phone1 varchar(20),--电话1
                                    email varchar(100),--邮箱
                                    email1 varchar(100),--邮箱1
                                    create_person varchar(100),--创建人id
                                    create_time TIMESTAMP --创建时间
                                )'''
    # 事件记录表--富文本形式
    __table_create_person_record = '''create table if not exists person_record (
                                    idkey varchar(100) PRIMARY KEY, --主键
                                    belong_type int,--记录所属：1成员，2家庭，3家族
                                    belong_idkey  varchar(100),--记录所属索引-主键，成员对应成员主键，家族对应家族主键
                                    level int,--记录的重要级别，数字越小级别越高
                                    datetime TIMESTAMP,--记录日期时间
                                    subject varchar(500),--主题
                                    remark varchar(500),--简介
                                    base_image_id varchar(500),--预览图id
                                    type int default 5,--记录类型： 1文字 2图片 3视频 4音频 5富文本
                                    create_person varchar(100), --创建人
                                    create_time TIMESTAMP, --创建时间
                                    content text--记录内容
                                )'''

    # 成员关系表
    __table_create_person_relation = '''create table if not exists person_relation (
                                        idkey varchar(100) PRIMARY KEY, --主键
                                        person_idkey  varchar(100),--关系成员主键
                                        person_add_idkey  varchar(100),--被关系成员主键
                                        type int,--被关系人与关系人的关系类型,1夫，2妻，3父，4母，5子，6女，7兄，8弟，9姐，10妹
                                        relation_name  varchar(100),---关系名称
                                        create_person varchar(100), --创建人
                                        create_time TIMESTAMP, --创建时间
                                        remark text --简介
                                    )'''

    # 家族表
    __table_create_person_clan = '''create table if not exists person_clan (
                                            idkey varchar(100) PRIMARY KEY, --主键
                                            clan_name  varchar(100),--家族名称
                                            person_m_idkey varchar(100), --家族初始成员主键-夫
                                            person_f_idkey varchar(100), --家族初始成员主键-妻
                                            create_person varchar(100), --创建人
                                            create_time TIMESTAMP, --创建时间
                                            remark  text--简介
                                        )'''
    # 家庭表
    __table_create_person_family = '''create table if not exists person_family (
                                            idkey varchar(100) PRIMARY KEY, --主键
                                            family_name  varchar(100),--家庭名称
                                            person_m_idkey varchar(100), --家庭初始成员主键-夫
                                            person_f_idkey varchar(100), --家庭初始成员主键-妻
                                            create_person varchar(100), --创建人
                                            create_time TIMESTAMP, --创建时间
                                            remark  text--简介
                                        )'''

    # 资源表
    __table_create_person_resource = '''create table if not exists person_resource (
                                            idkey varchar(100) PRIMARY KEY, --主键
                                            upload_person varchar(100),--上传人主键
                                            resource_name  varchar(100),--资源名称
                                            resource_type int,--资源类型： 1文字 2图片 3视频 4音频 5富文本
                                            resource_path varchar(500),--资源地址
                                            create_person varchar(100), --创建人
                                            create_time TIMESTAMP, --创建时间
                                            remark  text--简介
                                        )'''

    def __init__(self):
        self.conn = None
        self.__initConn()
        self.cursor = None
        self.__init_db()

    def __initConn(self):
        self.conn = sqlite3.connect(self.__dbName)

    def __checkConnCur(self):
        if self.conn.close:
            self.__initConn()
        self.cursor = self.conn.cursor()

    def __closeConnCur(self):
        # if self.cursor.close is not True:
        #     self.cursor.close()
        if self.conn.close is not True:
            self.conn.close()

    def __initSettingInfo(self):
        self.__checkConnCur()
        get_data = '''select si.info_name from settings_info si;'''
        set_data = '''insert into settings_info(info_name,info_value) values ('log_file_path',''),
                    ('vkms_file_path',''),('test_guide_url',''),('jekins_url','');'''
        try:
            self.cursor.execute(get_data)
            rows = self.cursor.fetchall()
            print("查询settingInfo-ok")
            if len(rows) == 0:
                self.cursor.execute(set_data)
                self.conn.commit()
                print("初始化setting-ok")
        except Exception as e:
            print("查询settingInfo失败-->" + str(e))
        finally:
            self.__closeConnCur()

    def getRowFields(self):
        fieldnames = []
        if self.cursor is not None:
            fieldnames = [desc[0] for desc in self.cursor.description]
        return fieldnames

    def executeSqlMakeRowsDataToArrayMap(self, sql):
        rowDatas = []
        if self.cursor is not None:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            fieldnames = self.getRowFields()
            if len(rows) > 0:
                for row in rows:
                    row_one = {}
                    for fieldIndex in range(len(fieldnames)):
                        row_one[fieldnames[fieldIndex]] = row[fieldIndex]
                    rowDatas.append(row_one)
        return rowDatas

    def __init_db(self):
        self.__checkConnCur()
        try:
            self.cursor.execute(self.__table_create_person_info)
            self.cursor.execute(self.__table_create_person_record)
            self.cursor.execute(self.__table_create_person_relation)
            self.cursor.execute(self.__table_create_person_clan)
            self.cursor.execute(self.__table_create_person_family)
            self.cursor.execute(self.__table_create_person_resource)
            # self.__initSettingInfo()
            print("数据库初始化完成1")
        except Exception as e:
            print("数据库初始化失败1" + str(e))
        finally:
            self.__closeConnCur()

    # 登录
    def login(self, loginData):
        self.__checkConnCur()
        if (loginData is not None
                and loginData['login_name'] is not None
                and loginData['login_pwd'] is not None
                and "'" not in loginData['login_name']
                and "'" not in loginData['login_pwd']):
            login_sql = (f'''
            select p.* from person_info p where 
            p.login_name='{loginData['login_name']}' 
            and p.login_pwd='{loginData['login_pwd']}'
                        ''')
            try:
                rowDatas = self.executeSqlMakeRowsDataToArrayMap(login_sql)
                print("查询数据成功 login")
                # print(len(rows), rowDatas)
                return rowDatas
            except Exception as e:
                print("查询失败 login-->" + str(e))
                return False
            finally:
                self.__closeConnCur()
        else:
            return None

    # 添加一个成员
    def addPerson(self, personData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_info
                    (idkey, name,login_name,login_pwd,gender,remark,phone)
                    values (?,?,?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, personData)
            self.conn.commit()
            print("插入数据成功addPerson")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚addPerson-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 修改成员信息
    def updatePerson(self, personData):
        self.__checkConnCur()
        save_data = (f'''update person_info
        set 
        where idkey='{personData.idkey}' ''')
        try:
            self.cursor.execute(save_data, personData)
            self.conn.commit()
            print("修改数据成功updatePerson")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚updatePerson-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 添加一个记录
    def addRecord(self, recordData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_record
                       (idkey, belong_type, belong_idkey,level,datetime,
                       subject,remark,base_image_id,type,create_person,create_time,content)
                       values (?,?,?,?,?,?,?,?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, recordData)
            self.conn.commit()
            print("插入数据成功addRecord")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚addRecord-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    def getRecord(self, belong_idkey):
        self.__checkConnCur()
        get_data = (f'''select idkey, belong_type, belong_idkey,level,datetime,
                       subject,remark,base_image_id,type,create_person,create_time,content from person_record
                       where belong_idkey = '{belong_idkey}' order by create_time desc''')
        try:
            rowDatas = self.executeSqlMakeRowsDataToArrayMap(get_data)
            print("数据查询 getRecord")
            return rowDatas
        except Exception as e:
            self.conn.rollback()
            print("数据查询失败，getRecord-->" + str(e))
            return []
        finally:
            self.__closeConnCur()

    def updateRecord(self, recordData):
        self.__checkConnCur()
        update_data = f''' update person_record set subject='{recordData[1]}',remark='{recordData[2]}',
                        content='{recordData[3]}' where idkey='{recordData[0]}' '''
        try:
            self.cursor.execute(update_data)
            self.conn.commit()
            print("数据修改 updateRecord")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据修改失败，updateRecord-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

        # 添加一个关系
    def addRelation(self, recordData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_relation
                       (idkey, person_idkey, person_add_idkey,type,relation_name,remark)
                       values (?,?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, recordData)
            self.conn.commit()
            print("插入数据成功addRelation")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚addRelation-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 添加一个家族
    def addClan(self, recordData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_clan
                        (idkey, clan_name, person_m_idkey,person_f_idkey,remark)
                        values (?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, recordData)
            self.conn.commit()
            print("插入数据成功addClan")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚addClan-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 添加一个家庭
    def addFamily(self, recordData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_family
                        (idkey, family_name, person_m_idkey,person_f_idkey,create_person,create_time,remark)
                        values (?,?,?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, recordData)
            save_data_person1 = (
                f'''update person_info set family_idkey='{recordData[0][0]}' where idkey='{recordData[0][2]}' ''')
            save_data_person2 = (
                f'''update person_info set family_idkey='{recordData[0][0]}' where idkey='{recordData[0][3]}' ''')
            relationData = [(str(uuid.uuid4()), recordData[0][2], recordData[0][3], 2, "妻", "")]

            save_dataRelation = ('''INSERT INTO person_relation
                                   (idkey, person_idkey, person_add_idkey,type,relation_name,remark)
                                   values (?,?,?,?,?,?)''')
            self.cursor.execute(save_data_person1)
            self.cursor.execute(save_data_person2)
            self.cursor.executemany(save_dataRelation, relationData)
            self.conn.commit()
            print("插入数据成功 addFamily")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚 addFamily-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 添加一个资源
    def addResource(self, recordData):
        self.__checkConnCur()
        save_data = ('''INSERT INTO person_resource
                        (idkey, upload_person, resource_name, resource_type,resource_path,create_person,create_time,remark)
                        values (?,?,?,?,?,?,?,?)''')
        try:
            self.cursor.executemany(save_data, recordData)
            self.conn.commit()
            print("插入数据成功 addResource")
            return True
        except Exception as e:
            self.conn.rollback()
            print("数据插入失败，回滚 addResource-->" + str(e))
            return False
        finally:
            self.__closeConnCur()
        # 添加一个资源

    # 获取资源--根据条件
    def getResource(self, param):
        self.__checkConnCur()
        get_data = (f'''select idkey, upload_person, resource_name, resource_type,resource_path,create_person,
                        create_time,remark from person_resource
                        where create_time>={param['date'][0]}
                          and create_time<={param['date'][1]}
                           and create_person='{param['idkey']}' ''')
        try:
            rows_source = self.executeSqlMakeRowsDataToArrayMap(get_data)
            print("查询数据成功 getResource")
            for index in range(len(rows_source)):
                rows_source[index]['resource_path'] = rows_source[index]['resource_path'].replace(file_root_path,'')
            return rows_source
        except Exception as e:
            self.conn.rollback()
            print("查询失败，回滚 getResource-->" + str(e))
            return False
        finally:
            self.__closeConnCur()

    # 根据人员key查询家庭信息，所有成员信息，所有关系信息
    def selectFamilyPersonsByFamilyIdKey(self, personId):
        self.__checkConnCur()
        get_data = (f"select p.* from person_info p where p.idkey='{personId}'"
                    f" UNION select p.* from person_info p where p.idkey in "
                    f"(select r.person_add_idkey as p_key from person_relation r where r.person_idkey='{personId}')")
        try:
            rows_family = []
            rows_relation = []
            print(get_data)
            rows_person = self.executeSqlMakeRowsDataToArrayMap(get_data)
            if len(rows_person) > 0:
                get_data_family = (f''' select f.idkey, f.family_name,f.person_m_idkey,f.person_f_idkey,f.remark
                                                    from person_family f
                                                    where f.idkey='{rows_person[0]["family_idkey"]}'
                                                    ''')
                rows_family = self.executeSqlMakeRowsDataToArrayMap(get_data_family)
                if len(rows_family) > 0:
                    get_data_relation = (f'''
                    select r.idkey,r.person_idkey,r.person_add_idkey,r.type,r.relation_name, r.remark
                    from person_relation r
                    where r.person_idkey='{rows_family[0]["person_m_idkey"]}'
                    ''')
                    rows_relation = self.executeSqlMakeRowsDataToArrayMap(get_data_relation)
            return {'person': rows_person, 'family': rows_family, 'relation': rows_relation}
        except Exception as e:
            self.conn.rollback()
        finally:
            self.__closeConnCur()

    def getPersons(self):
        self.__checkConnCur()
        get_data = 'select p.idkey,p.name,p.gender from person_info p'
        self.cursor.execute(get_data)
        rows_person = self.cursor.fetchall()
        self.__closeConnCur()
        return rows_person

    # 根据成员查询其所在的家庭，--可能是1个也可能是两个
    def getFamilyByPerson(self, personId):
        self.__checkConnCur()
        family = []
        get_data_family = (f'''select f.family_name,f.person_m_idkey,f.person_f_idkey,f.remark
                                    from person_family f
                                    where f.person_m_idkey='{personId}
                                    or f.person_f_idkey='{personId}'
                                    ''')
        try:
            family = self.executeSqlMakeRowsDataToArrayMap(get_data_family)
        except Exception as e:
            self.conn.rollback()
        finally:
            self.__closeConnCur()
        return family
    # def checkRepeatInfo(self, sTime, eTime, elapsed, testId):
    #     self.__checkConnCur()
    #     get_data = (f"select count(li.test_id) as count from log_info li where "
    #                 f"li.start_time='{sTime}' and li.end_time='{eTime}' "
    #                 f"and li.elapsed='{elapsed}' and li.test_id='{testId}'")
    #     print('checkRepeatInfo---')
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         self.conn.rollback()
    #     finally:
    #         self.__closeConnCur()
    #
    # def check_VKMSRepeatInfo(self, vkms):
    #     self.__checkConnCur()
    #     get_data = (f"select count(li.id_key) as count from rt_vkms li where "
    #                 f"li.target_name='{vkms[1]}' and li.log_file_id='{vkms[7]}' ")
    #     print(f'checkVKMSRepeatInfo---{get_data}')
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         self.conn.rollback()
    #     finally:
    #         self.__closeConnCur()
    #
    # def save_VKMS(self, vkms):
    #     self.__checkConnCur()
    #     save_data = ('''INSERT INTO rt_vkms
    #             (id_key, target_name,target_vkms, target_rat, target_r_p, target_connect, received_time, log_file_id)
    #             values (?,?,?,?,?,?,?,?)''')
    #     try:
    #         self.cursor.executemany(save_data, vkms)
    #         self.conn.commit()
    #         print("插入数据成功2")
    #         return True
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("数据插入失败，回滚2-->" + str(e))
    #         return False
    #     finally:
    #         self.__closeConnCur()
    #
    # def save_VKMS_speed(self, datas):
    #     self.__checkConnCur()
    #     strJoin = ","
    #     save_data = (f'''INSERT INTO rt_vkms_speed
    #                 (id_key, target_id_key, received_time, apn_1_speed, apn_2_speed)
    #                 values {strJoin.join(datas)}''')
    #     try:
    #         self.cursor.execute(save_data)
    #         self.conn.commit()
    #         print("插入数据成功3")
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("数据插入失败，回滚3-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def save_log_details(self, datas):
    #     self.__checkConnCur()
    #     save_data = (f'''INSERT INTO log_info_detail
    #                 (id_key, test_id, log_detail)
    #                 values {datas}''')
    #     try:
    #         self.cursor.execute(save_data)
    #         self.conn.commit()
    #         print("插入数据成功3")
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("数据插入失败，回滚3-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def get_vkms_data(self):
    #     self.__checkConnCur()
    #     get_data = '''select
    #                 rv.id_key,
    #                 rv.log_file_id,
    #                 rv.received_time,
    #                 rv.target_connect,
    #                 rv.target_name,
    #                 rv.target_r_p,
    #                 rv.target_rat,
    #                 rv.target_vkms
    #             from
    #                 rt_vkms rv;'''
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         print("查询数据成功4")
    #         print(rows)
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败4-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def get_vkms_speed_data(self, targetId):
    #     self.__checkConnCur()
    #     get_data = f'''select
    #                 rvs.apn_1_speed,
    #                 rvs.apn_2_speed,
    #                 rvs.id_key,
    #                 rvs.received_time,
    #                 rvs.target_id_key
    #             from
    #                 rt_vkms_speed rvs where rvs.target_id_key='{targetId}';'''
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         print("查询数据成功41")
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败41-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def save_data(self, datas):
    #     self.__checkConnCur()
    #     save_data = ('''INSERT INTO log_info
    #                 (id_key, test_id, name, label, total, pass, fail, skip, start_time, end_time, elapsed, status,
    #                 type, save_time, file_id,file_path)
    #                 values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')
    #     try:
    #         self.cursor.executemany(save_data, datas)
    #         self.conn.commit()
    #         print("插入数据成功5")
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("数据插入失败，回滚5-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def get_data(self):
    #     self.__checkConnCur()
    #     get_data = ('select id_key, test_id, name, label, total, pass, fail, skip, start_time, end_time, elapsed, '
    #                 'status,type, save_time, file_id, file_path from log_info')
    #     try:
    #         rows = self.cursor.executescript(get_data)
    #         print("查询数据成功6")
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败6-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def getAutomationAllCaseName(self):
    #     self.__checkConnCur()
    #     get_data = "select log.id_key, log.name from log_info log group by log.name"
    #     try:
    #         self.cursor.execute(get_data)
    #         print("查询数据成功9")
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败9-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def getAutomationResultWithParam(self, caseCode):
    #     self.__checkConnCur()
    #     get_data = ('select log.id_key, log.test_id, log.name, log.label, log.total, log.pass, log.fail, log.skip,'
    #                 'log.start_time, log.end_time, log.elapsed, log.status,log.type, log.save_time, log.file_id,'
    #                 ' detail.log_detail ,log.file_path from log_info log, log_info_detail detail'
    #                 f' where log.id_key = detail.test_id and LOWER(log.name)=LOWER(\'{caseCode}\')')
    #     try:
    #         self.cursor.execute(get_data)
    #         print("查询数据成功8")
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败8-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def getAutomationResult(self):
    #     self.__checkConnCur()
    #     get_data = ('select log.id_key, log.test_id, log.name, log.label, log.total, log.pass, log.fail, log.skip,'
    #                 'log.start_time, log.end_time, log.elapsed, log.status,log.type, log.save_time, log.file_id,'
    #                 ' detail.log_detail ,log.file_path from log_info log, log_info_detail detail'
    #                 ' where log.id_key = detail.test_id and LOWER(log.name) like \'%backendcheck%\'')
    #     try:
    #         self.cursor.execute(get_data)
    #         print("查询数据成功7")
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         print("数据查询失败7-->" + str(e))
    #     finally:
    #         self.__closeConnCur()
    #
    # def setSettingInfo(self, datas):
    #     self.__checkConnCur()
    #     save_data = f'''update settings_info set info_value='{datas[0]}' where info_name='log_file_path';'''
    #     save_data1 = f'''update settings_info set info_value='{datas[1]}' where info_name='vkms_file_path';'''
    #     save_data2 = f'''update settings_info set info_value='{datas[2]}' where info_name='test_guide_url';'''
    #     save_data3 = f'''update settings_info set info_value='{datas[3]}' where info_name='jekins_url';'''
    #     try:
    #         self.cursor.execute(save_data)
    #         self.cursor.execute(save_data1)
    #         self.cursor.execute(save_data2)
    #         self.cursor.execute(save_data3)
    #         self.conn.commit()
    #         print("save setting ok")
    #         return True
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("save setting 失败" + str(e))
    #         return False
    #     finally:
    #         self.__closeConnCur()
    #
    # def getSettingInfo(self):
    #     self.__checkConnCur()
    #     get_data = f'''select info_name,info_value from settings_info;'''
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         print("getSettingInfo ok")
    #         return rows
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("getSettingInfo 失败" + str(e))
    #         return []
    #     finally:
    #         self.__closeConnCur()
    #
    # def get_vkms_speed_data_all(self):
    #     self.__checkConnCur()
    #     get_data = f'''select
    #                 rvs.apn_1_speed,
    #                 rvs.apn_2_speed,
    #                 rvs.id_key,
    #                 rvs.received_time,
    #                 rvs.target_id_key
    #             from
    #                 rt_vkms_speed rvs;'''
    #     try:
    #         self.cursor.execute(get_data)
    #         rows = self.cursor.fetchall()
    #         print("getSettingInfo ok")
    #         return rows
    #     except Exception as e:
    #         self.conn.rollback()
    #         print("getSettingInfo 失败" + str(e))
    #         return []
    #     finally:
    #         self.__closeConnCur()
