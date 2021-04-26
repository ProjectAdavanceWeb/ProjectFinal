from flask.helpers import url_for
import pymongo
import bcrypt
from flask import Flask,jsonify,render_template,request,redirect,session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from bson import json_util

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:NSOtqh59246@node13008-atiwat-01-clone133880.app.ruk-com.cloud:11027") 
#client = pymongo.MongoClient("mongodb://admin:NSOtqh59246@10.100.2.64") #runoncloud

db = client["project"] 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/Car", methods=['GET','POST','PUT'])
def get_allCar():
    char = db.customer #เป็นเหมือนการนำค่าชื่อหัวตารางมาใส่ในตัวแปร char
    output = []
    for x in char.find(): #ทำตามฟังชั่น
        output.append({'_id' : x['_id'],'username' : x['username'],'email' : x['email'],
                        'password' : x['password']}) #เอาค่าในตารางมาอ่านแล้วใส่ไปใน output เป็นเหมือนค่าอาเร
    return json_util.dumps(output) #หลังจากทำเงื่อนไขเสร็จส่งค่ากลับไปที่ output

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
    return render_template("contact.html",ses=ses)

# ############################################################################################
@app.route("/showdata")
def showdata():
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
        data = session['email'] + session['username'] + session['password'] + session['phone'] + session['address'] 
    return render_template("showdata.html",ses=ses, data = data)
# ####################################################################################

@app.route("/admincontact")
def admincontact():
    emp_list = db.contact.find()
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
    return render_template("AdminContact.html",ses=ses , emp_list = emp_list)

@app.route("/admincustomer")
def admincustomer():
    emp_list = db.customer.find()
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
    return render_template("AdminCustomer.html",ses=ses , emp_list = emp_list)


@app.route("/menu")
def menu():
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
    return render_template("menu.html" , ses = ses)

@app.route('/insertcontact', methods=['POST'])
def insertcontact():
  char = db.contact
  cname = request.form['cname'] 
  cemail = request.form['cemail']
  cmessage = request.form['cmessage']

  char.insert_one({ 'cname' : cname, 'cemail' : cemail, 'cmessage': cmessage})
  return render_template('contact.html')

@app.route("/Register")
def Register():
    return render_template("Register.html")


@app.route('/loginBackend', methods=['POST'])
def loginBackend():
    users = db.customer
    email = request.form.get("email")
    password = request.form.get("password")
    login_user = users.find_one({'email': request.form['email']})

    if email == "admin":
        email_val = login_user['email']
        passwordcheck = login_user['password']

        if bcrypt.checkpw(password.encode('utf-8'),passwordcheck):
            session['email'] = request.form['email']
            return redirect(url_for('admincontact'))

    elif login_user:
        email_val = login_user['email']
        passwordcheck = login_user['password']

        if bcrypt.checkpw(password.encode('utf-8'),passwordcheck):
            session['email'] = request.form['email']
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['phone'] = request.form['phone']
            session['address'] = request.form['address']
            return redirect(url_for('menu'))
        return render_template('index.html')    
    else : 
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    char = db.customer
    if request.method == 'POST':
        users = char
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            emaila = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            users.insert_one({'username' : request.form['username'], 'password' : hashpass , 'email':emaila, 'phone':phone, 'address':address })
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        
        return 'Invalid email or password'

    return render_template('Register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
