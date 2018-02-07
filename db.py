import sqlite3

DISABLED = 'Disabled'  # 禁用
ENABLE = 'enable'  # 开启全部功能
SIMPLE = 'simple'  # 开启群管理功能
DB_NAME = 'qq.db'

create_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS follow 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, number INT,type TEXT); 
        '''
try:
    conn = sqlite3.connect(DB_NAME)
    conn.execute(create_tb_cmd)
finally:
    conn.close()


def connect():
    """
    获取到数据库的连接对象，参数为数据库文件的绝对路径
        如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
        路径下的数据库文件的连接对象；否则，返回内存中的数据接
        连接对象
    """
    return sqlite3.connect(DB_NAME)


def insert_dt(number, type):
    db = connect()
    c = db.cursor()
    success = False
    sql = """ INSERT INTO follow (number, type) VALUES (%d,"%s"); """ % (number, type)
    try:
        c.execute(sql)
        db.commit()
        success = True
    except:
        success = False
    finally:
        c.close()
        db.close()
        return success


def select_all():
    db = connect()
    c = db.cursor()
    list = []
    try:
        cursor = c.execute("SELECT number, type FROM follow;")
        for row in cursor:
            list.append({"number": row[0], "type": row[1]})
    finally:
        c.close()
        db.close()
        print(list)
        return list


def select(number, type):
    db = connect()
    c = db.cursor()
    success = ""
    try:
        cursor = c.execute("SELECT * FROM follow WHERE number=%d;" % number)
        if cursor.fetchall():
            if type == DISABLED:
                delete(number)
                success = "本群已禁用"
            elif update(number, type):
                success = "本群已切换到" + ["全功能", "简单"][type != ENABLE] + "模式"
        else:
            if insert_dt(number, type):
                success = "本群已开启" + ["全功能", "简单"][type != ENABLE] + "模式"
    finally:
        c.close()
        db.close()
        return success


def delete(number):
    db = connect()
    c = db.cursor()
    success = False
    try:
        c.execute("DELETE from follow WHERE number=%d;" % number)
        db.commit()
        success = True
    except:
        success = False
    finally:
        c.close()
        db.close()
        return success


def update(number, type):
    db = connect()
    c = db.cursor()
    success = False
    try:
        c.execute("UPDATE follow SET type='%s' WHERE (number=%d);" % (type, number))
        db.commit()
        success = True
    except:
        success = False
    finally:
        c.close()
        db.close()
        return success


def select_sensitive_all():
    db = connect()
    c = db.cursor()
    list = []
    try:
        cursor = c.execute("SELECT content FROM sensitive ")
        for row in cursor:
            list.append(row[0])
    finally:
        c.close()
        db.close()
        return list




if __name__ == '__main__':
    # update(6965717, ALLOW)
    # update(6965717, SIMPLE)
    select_all()
