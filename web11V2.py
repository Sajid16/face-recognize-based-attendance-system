from flask import *
from face import facerecognitionFunction
from facedetect import facedetection
from facedetectReg import facedetectionReg
from faceReg import facerecognitionReg
import os
import csv
import cx_Oracle
import time
from datetime import datetime
import uuid
import cv2
import random

# Path for recognizing image(uploaded image for recognizing. Image replace every 5 sec.)
PATH_TO_TEST_IMAGES_DIR = './check_images'
SAVED_IMAGES = './saved_images'
VERIFY_IMAGES = './verify_images'

dsn_tns = cx_Oracle.makedsn('10.11.201.51', '1521', 'APEXTEST')
conn = cx_Oracle.connect(user='PATTNDB', password='pattndb', dsn=dsn_tns)

try:
    os.mkdir(PATH_TO_TEST_IMAGES_DIR)
    os.mkdir(SAVED_IMAGES)
    os.mkdir(VERIFY_IMAGES)
except FileExistsError:
    pass

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/recognition')
def recognition():
    if 'branch_code' in session:
        branch_code = session['branch_code']
    my_dict = {'branch_code': branch_code}
    return render_template('getImage3.html', my_dict=my_dict)


# @app.route('/recognition')
# def recognition():
#     if 'company_code' not in session or 'user_id' not in session:
#         return render_template('failauth.html')
#     elif 'company_code' in session and 'user_id' in session and 'branch' in session:
#         company_code = session['company_code']
#         user_id = session['user_id']
#         branch = session['branch']
#         # my_dict = {'company_code': company_code, 'user_id': user_id, 'branch_name': branch_name}
#         my_dict = {'company_code': company_code, 'user_id': user_id, 'branch': branch}
#         # print(my_dict)
#         return render_template('getImage2.html', my_dict=my_dict)


# @app.route('/recognition1/<string:company_code>/<string:user_id>/<string:token>')
# def check_auth_recognition(company_code, user_id, token):
#     authentication_result = ''
#     conn_auth = conn.cursor()
#     authentication_result = conn_auth.callproc("PATTNDB.DPR_FACE_RECO_VALID_Call",
#                                                [company_code, user_id, token, authentication_result])
#     authentication_result = authentication_result[-1]
#     session['token'] = token
#     if authentication_result == 'Y':
#         session['company_code'] = company_code
#         session['user_id'] = user_id
#         return redirect(url_for('test'))
#     else:
#         return redirect(url_for('test'))


@app.route('/registration/<string:company_code>/<string:user_id>/<string:token>')
def check_auth_registration(company_code, user_id, token):
    authentication_result = ''
    conn_auth = conn.cursor()
    authentication_result = conn_auth.callproc("PATTNDB.DPR_FACE_RECO_VALID_Call",
                                               [company_code, user_id, token, authentication_result])
    authentication_result = authentication_result[-1]
    if authentication_result == 'Y':
        session['company_code'] = company_code
        session['user_id'] = user_id
        return render_template("geolocation.html")
    else:
        return render_template('failauth.html')


@app.route('/location', methods=['POST'])
def location():
    x = request.form.get("latitude")
    y = request.form.get("longitude")
    z = request.form.get("altitude")
    session['latitude'] = x
    session['longitude'] = y
    session['altitude'] = z
    # print(session['branch_code'])
    return redirect(url_for('registration'))


@app.route('/location_update', methods=['POST'])
def location_update():
    x = request.form.get("latitude")
    y = request.form.get("longitude")
    z = request.form.get("altitude")
    session['latitude'] = x
    session['longitude'] = y
    session['altitude'] = z
    # print(session['branch_code'])
    return redirect(url_for('update_registration'))


@app.route('/update_registration/<string:company_code>/<string:user_id>/<string:token>')
def check_auth_update_registration(company_code, user_id, token):
    authentication_result = ''
    conn_auth = conn.cursor()
    authentication_result = conn_auth.callproc("PATTNDB.DPR_FACE_RECO_VALID_Call",
                                               [company_code, user_id, token, authentication_result])
    authentication_result = authentication_result[-1]
    if authentication_result == 'Y':
        session['company_code'] = company_code
        session['user_id'] = user_id
        return render_template("geolocation_update.html")
    else:
        return render_template('failauth.html')


@app.route('/registration')
def registration():
    if 'company_code' not in session or 'user_id' not in session:
        return render_template('failauth.html')
    else:
        select_officecode = conn.cursor()
        select_officecode.execute("select * from VW_PYCODMAS")
        branch_name = []
        for row in select_officecode:
            branch_name.append(row[3])
        company_code = session['company_code']
        user_id = session['user_id']
        my_dict = {'company_code': company_code, 'user_id': user_id, 'branch': branch_name}
        return render_template('registration.html', my_dict=my_dict)


@app.route('/update_registration')
def update_registration():
    if 'company_code' not in session or 'user_id' not in session:
        return render_template('failauth.html')
    else:
        select_officecode = conn.cursor()
        select_officecode.execute("select * from VW_PYCODMAS")
        branch_name = []
        for row in select_officecode:
            branch_name.append(row[3])
        company_code = session['company_code']
        user_id = session['user_id']
        my_dict = {'company_code': company_code, 'user_id': user_id, 'branch': branch_name}
        return render_template('update_registration.html', my_dict=my_dict)


@app.route('/image_saved', methods=['GET', 'POST'])
def image_saved():
    try:
        i = request.files['image']  # get the image
        eid = str(request.form.get('emp'))
        branch_code = str(request.form.get('branch_code'))
        lat = session['latitude']
        lon = session['longitude']
        alt = session['altitude']
        p = conn.cursor()
        stmnt = "select PYHDRCDE,PYSOFCDE from VW_PYCODMAS where PYCODDES = '" + branch_code + "'"
        p.execute(stmnt)
        officecode = ''
        for row in p:
            officecode = row[0] + row[1]
        print('office value: ' + officecode)
        ip = str(request.form.get('ip'))
        conn_eidcheck = conn.cursor()
        conn_eidcheck.execute("select count(EMPCDE) from register where EMPCDE= '" + eid + "' ")
        for row in conn_eidcheck:
            if row[0] == 0:
                key = 1
                break
            else:
                key = 0
                break
        compcde = str(request.form.get('compcde'))
        time = datetime.now().strftime('%m/%d/%Y %H:%M:%S %p')

        if key == 1:
            eid_save = compcde + '_' + eid
            f = eid_save + '.jpeg'
            try:
                os.mkdir(VERIFY_IMAGES + '/' + officecode)
            except FileExistsError:
                pass
            i.save('%s/%s' % (VERIFY_IMAGES + '/' + officecode, f))

            # facedetect code before register
            facedetect = facedetectionReg(f, officecode)
            if facedetect == 1:
                facerecog = facerecognitionReg(f, officecode)
                if facerecog == 0:
                    try:
                        os.mkdir(SAVED_IMAGES + '/' + officecode)
                    except FileExistsError:
                        pass
                    img = cv2.imread(VERIFY_IMAGES + '/' + officecode + "/" + f)
                    cv2.imwrite(os.path.join(SAVED_IMAGES + '/' + officecode + "/" + f), img)
                    user_id = session['user_id']
                    conn_insert = conn.cursor()
                    stmnt = "insert into register (EMPCDE, COMPCDE, REG_TIME, USER_ID, ip_address,OFFCDE, LATITUDE,LONGITUDE)" \
                            "values('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')"
                    stmnt = stmnt.format(eid, compcde, time, user_id, ip, officecode, lat, lon)
                    conn_insert.execute(stmnt)
                    conn.commit()

                    image_insert = conn.cursor()
                    with open(SAVED_IMAGES + '/' + officecode + "/" + f, 'rb') as k:
                        imgdata = k.read()
                    image_insert.execute(
                        """insert into SAVED_IMAGES (EMPCDE, COMPCDE, IMAGE) values (:eid, :compid, :blobdata)""",
                        eid=eid, compid=branch_code, blobdata=imgdata)
                    conn.commit()
                    os.remove(VERIFY_IMAGES + '/' + officecode + "/" + f)
                    return 'ok'
                elif facerecog == 1:
                    os.remove(VERIFY_IMAGES + "/" + officecode + "/" + f)
                    return "image_already_registered"
            elif facedetect > 1:
                os.remove(VERIFY_IMAGES + '/' + officecode + "/" + f)
                return "multipleface"
            else:
                os.remove(VERIFY_IMAGES + '/' + officecode + "/" + f)
                return "noface"
        elif key == 0:
            return 'fail'
    except:
        return 'except found in /image_saved path'


@app.route('/update_image_saved', methods=['GET', 'POST'])
def update_image_saved():
    try:
        i = request.files['image']  # get the image
        eid = str(request.form.get('emp'))
        branch_code = str(request.form.get('branch_code'))
        lat = session['latitude']
        lon = session['longitude']
        company_code = session['company_code']
        # alt = session['altitude']
        p = conn.cursor()
        stmnt = "select PYHDRCDE,PYSOFCDE from VW_PYCODMAS where PYCODDES = '" + branch_code + "'"
        p.execute(stmnt)
        officecode = ''
        for row in p:
            officecode = row[0] + row[1]
        print('office value: ' + officecode)

        ip = str(request.form.get('ip'))
        conn_eidcheck = conn.cursor()
        conn_eidcheck.execute("select count(EMPCDE) from register where EMPCDE= '" + eid + "' ")
        for row in conn_eidcheck:
            if row[0] == 0:
                key = 1
                break
            else:
                key = 0
                break
        compcde = str(request.form.get('compcde'))
        time = datetime.now().strftime('%m/%d/%Y %H:%M:%S %p')
        if key == 0:
            past_off = conn.cursor()
            stmnt = "select OFFCDE from register where EMPCDE = '" + eid + "'"
            past_off.execute(stmnt)
            for row in past_off:
                past_offcde = row[0]
            past_image_path = company_code + "_" + eid

            if past_offcde != officecode:
                os.remove('./saved_images/' + past_offcde + "/" + past_image_path + ".jpeg")

            eid_save = compcde + '_' + eid
            f = eid_save + '.jpeg'
            try:
                os.mkdir(SAVED_IMAGES + '/' + officecode)
            except FileExistsError:
                pass
            i.save('%s/%s' % (SAVED_IMAGES + '/' + officecode, f))
            # facedetect code update register
            facedetect = facedetectionReg(f, officecode)
            if facedetect == 1:
                print("face detected")
                user_id = session['user_id']
                conn_insert = conn.cursor()
                stmnt = "update register set REG_TIME = '" + time + "', ip_address = '" + ip + "', " \
                                                                                               "OFFCDE = '" + officecode + "', LATITUDE='" + lat + "', LONGITUDE='" + lon + "' " \
                                                                                                                                                                            "where EMPCDE = '" + eid + "'"
                conn_insert.execute(stmnt)
                conn.commit()
                return 'ok'
            elif facedetect > 1:
                os.remove('./saved_images/' + officecode + "/" + f)
                return "multipleface"

            else:
                os.remove('./saved_images/' + officecode + "/" + f)
                return "noface"
        else:
            return 'fail'
    except:
        return 'except found in /update image_saved path'


@app.route('/image', methods=['GET', 'POST'])
def image():
    try:
        if "image_check_name" in session:
            image_check_name = session["image_check_name"]
        msg = ''
        i = request.files['image']  # get the image
        branch_code = ''
        branch_code = str(request.form.get('branch_code'))
        ip = str(request.form.get('ip'))
        # compcde = str(request.form.get('compcde'))
        # officecode = str(request.form.get('officecode'))
        lat = session['latitude']
        lon = session['longitude']
        f = image_check_name + '.jpeg'
        i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))

        # facedetect = facedetection(f)
        # if facedetect == 1:
        # print("face detected")

        # flag, empcde, status_flag, device, blink = facerecognitionFunction(f, branch_code, ip, lat, lon)
        flag, empcde, status_flag, device = facerecognitionFunction(f, branch_code, ip, lat, lon)
        # flag, empcde, status_flag = facerecognitionFunction(f, branch_code, ip, lat, lon)
        # print()
        print("flag: ", flag)
        print("status: ", status_flag)
        print("device: ", device)
        # print("blink: ", blink)

        # if flag == 1 and status_flag == 1 and device == 0 and blink == 1:
        if flag == 1 and status_flag == 1 and device == 0:
            msg = 'face_recognized/' + empcde
            return msg
        elif device == 1:
            return 'device_found'

        else:
            return 'face_unrecognized'
    except:
        return 'except found in /image path'


@app.route('/')
def test():
    session["image_check_name"] = uuid.uuid4().hex
    select_officecode = conn.cursor()
    select_officecode.execute("select * from VW_PYCODMAS")
    branch_name = []
    for row in select_officecode:
        branch_name.append(row[3])
    return render_template('select_branch.html', branch={'branch': branch_name})


@app.route('/handle_branch_code', methods=['POST'])
def handle_branch_code():
    branch_code = str(request.form.get('branch_code'))
    session['branch_code'] = branch_code
    x = request.form.get("latitude")
    y = request.form.get("longitude")
    z = request.form.get("altitude")
    session['latitude'] = x
    session['longitude'] = y
    session['altitude'] = z

    # print(session['branch_code'])
    return redirect(url_for('recognition'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))

    # app.run(host='10.11.201.67', port=5000)

    # app.run(ssl_context=('cert.pem', 'key.pem'))
