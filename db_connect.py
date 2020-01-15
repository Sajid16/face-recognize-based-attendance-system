import cx_Oracle
import datetime
import cv2
import os
dsn_tns = cx_Oracle.makedsn('10.11.201.51', '1521', 'APEXTEST')
conn = cx_Oracle.connect(user='PATTNDB', password='pattndb', dsn=dsn_tns)


c = conn.cursor()
officecode = 'LC004'
emp = '42'
f = '117_5645.jpeg'
SAVED_IMAGES = './saved_images' + '/' + officecode + "/" + f

with open(SAVED_IMAGES, 'rb') as k:
    imgdata = k.read()
    print(imgdata)

c.execute("""
        insert into SAVED_IMAGES (EMPCDE, COMPCDE, IMAGE)
        values (:eid, :compid, :blobdata)""",
        eid=emp, compid=officecode, blobdata=imgdata)
conn.commit()


# compcde = '1'
# empcde = '1'
# ip = '1'
#
# log_time = datetime.datetime.now()

# log_time = datetime.datetime.now().strftime('%m/%d/%Y:%H:%M:%S %p')
# print(log_time)

# log_time = datetime.datetime.strptime(log_time, '%m/%d/%Y %H:%M:%S %p')
# print(type(log_time))

# log_time = log_time.date()
# print(log_time)
# c = conn.cursor()
# stmnt = "insert into ATTN_LOG (COMPCDE, EMPCDE, IP_ADDRESS, LOG_TIME) Values '"+compcde+"', '"+empcde+"', '"+ip+"', " \
#                                 "to_date('"+str(log_time)+"', 'yyyy/mm/dd:hh:mi:ssam')"
# c.execute(stmnt)
# conn.commit()
# print(log_time)
# c.prepare("INSERT INTO ATTN_LOG VALUES(:t_val)")
# c.setinputsizes(t_val=cx_Oracle.TIMESTAMP)
# stmnt = "insert into ATTN_LOG (COMPCDE, EMPCDE, IP_ADDRESS, LOG_TIME) " \
#         "values '"+compcde+"', '"+empcde+"', '"+ip+"', {'log_time':ts}"
#
# stmnt = stmnt.format(compcde, empcde, str(ip), log_time)
# c.execute(stmnt)
# conn.commit()

# ts = datetime.now()
# print(ts)
# c.prepare("INSERT INTO ATTN_LOG VALUES(:LOG_TIME)")
# c.setinputsizes(LOG_TIME=cx_Oracle.TIMESTAMP)
# c.execute({'LOG_TIME': ts})
# c.execute("INSERT INTO ATTN_LOG VALUES(:LOG_TIME)", {'LOG_TIME': ts})
# conn.commit()

# eid = "000283"
# past_offcde = conn.cursor()
# stmnt = "select OFFCDE from register where EMPCDE = '"+eid+"'"
# past_offcde.execute(stmnt)
# for row in past_offcde:
#     print(row[0])

# company_code = '117'
# user_id = '999999'
# token = '14877668344607'
#
# authentication_result = ''
# conn_auth = conn.cursor()
# authentication_result = conn_auth.callproc("PATTNDB.DPR_FACE_RECO_VALID_Call",
#                        [company_code, user_id, token, authentication_result])
# print(authentication_result)

# curs = conn.cursor()
# curs.execute("select * from VW_PYCODMAS")
# for row in curs:
#     print(row[3])

# branch_code = 'GATEWAY'
# EMPCDE = '000123'
# COMPCDE = '200'
# c = conn.cursor()
# stmnt = "select APPROVAL_FLG from REGISTER where EMPCDE = '" + EMPCDE + "' and COMPCDE = '" + COMPCDE + "'"
# # stmnt = "select * from ATTN_LOG"
# c.execute(stmnt)
# for row in c:
#     print(row[0])


# conn.close()
# c = conn.cursor()
# p = c.execute("select * from ATTN_LOG")
#
# print(p)
# SAVED_IMAGES = './saved_images'
#
# stmnt = "insert into ATTN_LOG (LOG_TERMINAL, CREATEBY) values('{0}','{1}')"
# stmnt = stmnt.format(SAVED_IMAGES, 'hhhhh')
# c.execute(stmnt)
# conn.commit()

# for row in c:
#     info = row[0], '-', row[:-1]
# print(info)

# statement = "select id, name, age, notes from cx_people where name= '" + person_name + "'"
# eid = 'hhh'
# id_check = "select * from register where EMPCDE= '" + eid + "' "
# id_check = "select * from ATTN_LOG "

# o = c.execute(id_check)
# print(o)
conn.close()


'''
image_insert = conn.cursor()
                    with open(SAVED_IMAGES, 'rb') as k:
                        imgdata = k.read()
                        print(imgdata)

                    image_insert.execute("""
                            insert into SAVED_IMAGES (EMPCDE, COMPCDE, IMAGE)
                            values (:eid, :compid, :blobdata)""",
                              eid=eid, compid=branch_code, blobdata=imgdata)
                    conn.commit()

'''