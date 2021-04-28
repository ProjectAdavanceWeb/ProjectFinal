from flask.helpers import url_for
import pymongo
import bcrypt
from flask import Flask,jsonify,render_template,request,redirect,session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from bson import json_util
# Import ส่วนต่างๆเพื่อนำมาใช้งาน

app = Flask(__name__)
#client = pymongo.MongoClient("mongodb://admin:NSOtqh59246@node13008-atiwat-01-clone133880.app.ruk-com.cloud:11027") #run onlocal
client = pymongo.MongoClient("mongodb://admin:NSOtqh59246@10.100.2.64") #run on cloudRukcom ประกาศเพื่อทำการเชื่อมต่อกับ database 

db = client["project"] #ชื่อ database
app.secret_key = 'super secret key'  
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/showuser", methods=['GET','POST','PUT']) #ทำการเรียกใช้ หรือแก้ไขข้อมูลได้จากการเรียก route นี้
def showuser():
    char = db.customer #จะทำเรียกข้อมูลจาก table customer มาเก็บไว้ในตัวแปร char
    output = []
    for x in char.find(): # x จะทำการ loop ตามจำนวนของข้อมูลใน db
        output.append({'_id' : x['_id'],'username' : x['username'],'email' : x['email'],
                        'password' : x['password']}) #เอาค่าในตารางมาอ่านแล้วใส่ไปใน output 
    return json_util.dumps(output) #หลังจากทำเงื่อนไขเสร็จส่งค่ากลับไปที่ output

@app.route("/") #ทำการrouteหน้านี้เป็นหน้าแรก
def index():
    return render_template("index.html") #ทำการเรียกหน้า index

@app.route("/contact")  #ทำการrouteหน้า contact
def contact():
    if 'email' in session: #ทำการเช็ค session email 
        ses =  'You are logged in as ' + session['email'] #นำsession ของ email และข้อความเก็บไว้ในตัวแปร ses
    return render_template("contact.html",ses=ses) #ทำการเรียกหน้า contact และส่งตัวแปร ses

# ############################################################################################
# @app.route("/showdata")
# def showdata():
#     if 'email' in session:
#         ses =  'You are logged in as ' + session['email']
#         data = session['email'] + session['username'] + session['password'] + session['phone'] + session['address'] 
#     return render_template("showdata.html",ses=ses, data = data)
# ####################################################################################

@app.route("/admincontact") #ทำการrouteหน้า admincontact
def admincontact():
    emp_list = db.contact.find() # ค้นหาและดึงข้อมูลจาก db table contact ทั้งหมด ใส่ในตัวแปร emp_list
    if 'email' in session: #ทำการเช็ค session email 
        ses =  'You are logged in as ' + session['email'] #นำsession ของ email และข้อความเก็บไว้ในตัวแปร ses
    return render_template("AdminContact.html",ses=ses , emp_list = emp_list) #ทำการเรียกหน้า admincontact และส่งตัวแปร ses กับ emp_list

@app.route("/adminhome") #ทำการrouteหน้า adminhome
def adminhome():
    if 'email' in session: #ทำการเช็ค session email 
        ses =  'You are logged in as ' + session['email'] #นำsession ของ email และข้อความเก็บไว้ในตัวแปร ses
    return render_template("AdminHome.html",ses=ses ) #ทำการเรียกหน้า adminhome และส่งตัวแปร ses 

@app.route("/admincustomer") #ทำการrouteหน้า admincustomer
def admincustomer():
    emp_list = db.customer.find() # ค้นหาและดึงข้อมูลจาก db table customer ทั้งหมด ใส่ในตัวแปร emp_list
    if 'email' in session: #ทำการเช็ค session email 
        ses =  'You are logged in as ' + session['email'] #นำsession ของ email และข้อความเก็บไว้ในตัวแปร ses
    return render_template("AdminCustomer.html",ses=ses , emp_list = emp_list) #ทำการเรียกหน้า admincustomer และส่งตัวแปร ses กับ emp_list

@app.route('/delete') #ทำการrouteกับส่วน delete หน้า admincustomer
def delete():
    char = db.customer #จะทำเรียกข้อมูลจาก table customer มาเก็บไว้ในตัวแปร char
    key = request.values.get("username") # เรียกข้อมูล username มาเก็บไว้ใน key
    char.remove({"username": key}) #ทำการลบข้อมูล
    return redirect("/admincustomer") #จะทำการเรียกหน้า admincustomer


@app.route("/menu") #ทำการrouteหน้า menu
def menu():
    if 'email' in session: #ทำการเช็ค session email 
        ses =  'You are logged in as ' + session['email'] #นำsession ของ email และข้อความเก็บไว้ในตัวแปร ses
    return render_template("menu.html" , ses = ses) #ทำการเรียกหน้า menu และส่งตัวแปร ses 

@app.route('/insertcontact', methods=['POST']) #ส่วนของการ ส่งข้อมูลจาก user to admin โดยเรียกจาก form หน้า contact
def insertcontact():
  char = db.contact #จะทำเรียกข้อมูลจาก table contact มาเก็บไว้ในตัวแปร char
  cname = request.form['cname'] 
  cemail = request.form['cemail']
  cmessage = request.form['cmessage']
  #เก็บข้อมูลจาก form ไว้ในตัวแปรฝั่งซ้าย 

  char.insert_one({ 'cname' : cname, 'cemail' : cemail, 'cmessage': cmessage}) #จะทำการ insert ข้อมูลทั้งหมดลง database
  return render_template('contact.html') #จะทำการเรียกหน้า contact

@app.route("/Register") #ทำการrouteหน้า register
def Register():
    return render_template("Register.html") #ทำการเรียกหน้า register


@app.route('/loginBackend', methods=['POST']) #ส่วนของการ login โดยจะเรียกจากหน้า index
def loginBackend():
    users = db.customer #จะทำเรียกข้อมูลจาก table customer มาเก็บไว้ในตัวแปร users
    email = request.form.get("email")
    password = request.form.get("password")
    #เก็บข้อมูลจาก form ไว้ในตัวแปรฝั่งซ้าย
    login_user = users.find_one({'email': request.form['email']}) #ทำการรับข้อมูล email จาก form และนำมาค้นหาเพื่อเช็คกับรหัสบรรทัดล่าง และเก็บไว้ในตัวแปร login_user

    if email == "admin":  #เช็คว่า email นี้ใช่ admin หรือไม่
        email_val = login_user['email']
        passwordcheck = login_user['password'] #เก็บ password ไว้ในตัวแปร passwordcheck

        if bcrypt.checkpw(password.encode('utf-8'),passwordcheck): #เช็ครหัสและทำการเข้ารหัส password
            session['email'] = request.form['email'] #เก็บข้อมูล email ไว้ใน session email 
            return redirect(url_for('adminhome'))  #ถ้ารหัสถูกจะทำการเรียกหน้า adminhome

        return render_template("index.html") #ถ้ารหัสไม่ตรงจะทำการเรียกหน้า index

    elif login_user: #เช็คว่า email นี้ว่าตรงกับ เมลที่กรอกหรือไม่
        email_val = login_user['email']
        passwordcheck = login_user['password'] #เก็บ password ไว้ในตัวแปร passwordcheck

        if bcrypt.checkpw(password.encode('utf-8'),passwordcheck): #เช็ครหัสและทำการเข้ารหัส password
            session['email'] = request.form['email'] #เก็บข้อมูล email ไว้ใน session email
            return redirect(url_for('menu')) #ถ้ารหัสถูกจะทำการเรียกหน้า menu
        return render_template('index.html')    #ถ้ารหัสไม่ตรงจะทำการเรียกหน้า index
    else : 
        return render_template('index.html')    #ถ้ารหัสไม่ตรงเลยจะทำการเรียกหน้า index

@app.route('/register', methods=['POST', 'GET'])   #ส่วนของการ register โดยจะเรียกจากหน้า register
def register():
    char = db.customer #จะทำเรียกข้อมูลจาก table customer มาเก็บไว้ในตัวแปร char
    if request.method == 'POST':
        users = char
        existing_user = users.find_one({'email' : request.form['email']}) #เก็บค่า email จาก form จากการเช็คมาเก็บไว้ในตัวแปร existing_user

        if existing_user is None: #เอาตัวแปรมาเช็คว่าค่าว่างหรือไม่หรือซ้ำไหม ถ้าไม่จะเข้า if
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()) #เอารหัสมาทำการเข้าหัส
            emaila = request.form['email'] 
            phone = request.form['phone']
            address = request.form['address']
            #เอาค่าฝั่งซ้ายจาก form ที่รับมาเก็บไว้ในตัวแปรฝั่งซ้าย
            users.insert_one({'username' : request.form['username'], 'password' : hashpass , 'email':emaila, 'phone':phone, 'address':address }) #เก็บค่าทั้งหมดมา insert ไว้ใน database
            session['email'] = request.form['email'] #เก็บข้อมูล email ไว้ใน session email 
            return redirect(url_for('index')) #จะทำการเรียกหน้า index
        
        return 'Invalid email or password' #ถ้ารหัสซ้ำจะแสดงคำว่า Invalid email ....

    return render_template('Register.html')  #จะทำการเรียกหน้า register

@app.route('/logout') #เป็นการทำงานส่วนของ logout โดยเรียกมาจากเว็บที่มีการเรียก route นี้
def logout():
    session.pop('email', None) #การนำ email ออกจาก session
    return redirect(url_for('index')) #เรียกหน้า index


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    #รันโปรแกรม
