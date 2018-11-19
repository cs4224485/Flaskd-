# Author: harry.cai
# DATE: 2018/9/2
import pymysql


conn = pymysql.connect(
                    host='192.168.0.108',
                    port=3306,
                    user='harry',
                    password='123123',
                    db='Flask',
                    charset='utf8')

cursor = conn.cursor()

sql = "create table userinfo(nid int not null auto_increment primary key, username char(32),nickname char(32), code_id int)"

cursor.execute(sql)