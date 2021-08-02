from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
app = Flask(__name__)
app.secret_key="abz"
try:
    db=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_db"
    )
    if(db.is_connected()):
        print("connect")
except:
    print("unable of connect")

@app.route('/')
def hello_world():
    return "hello bhai"

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form["name"]
        password=request.form["password"]
        cur=db.cursor()
        cur.execute("SELECT * from studlogin WHERE studname =%s AND studpassword =%s", (name,password))
        result=cur.fetchall()
        if len(result) > 0:
            session["username"] = request.form["name"]
            print(session)
            print("here22")
            return redirect(url_for('detail'))
        cur.close()
    return render_template("login.html")


@app.route('/registry',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        cur = db.cursor()
        cur.execute("INSERT INTO studlogin (studname,studpassword) VALUES (%s,%s)",(name,password))
        db.commit()
        cur.close()
        return render_template("detailsdb.html")
    return render_template("registry.html")

@app.route('/details')
def detail():
        print(session)
        if session.get("username") =="":
            return redirect(url_for('login'))
        cur = db.cursor()
        cur.execute("SELECT * from stud")
        data=cur.fetchall()
        cur.close()
        return render_template("detailsdb.html",student=data,user=session.get("username"))

@app.route('/details',methods=['POST','GET'])
def update():
    if request.method == 'POST':

        if  request.form["btn"] == "updated":
            print("Up1")
            name= request.form["name"]
            marks=request.form["marks"]
            did=request.form["id"]
            cur = db.cursor()
            cur.execute("UPDATE stud set smark=%s ,sname=%s where sid=%s" ,(marks,name,did))
            db.commit()
            cur.close()
            return redirect(url_for('detail'))
        if request.form["btn"] == "delete":
            print("HERE")
            id=request.form["delete1"]
            print("here")
            print(id)
            cur = db.cursor()
            cur.execute("DELETE FROM stud WHERE sid= %s" % (id))
            db.commit()
            cur.close()
            return redirect(url_for('detail'))
        if request.form["btn"] == "Insert":
            print("IN")
            name = request.form["name"]
            marks = request.form["marks"]
            cur = db.cursor()
            cur.execute("INSERT INTO stud (sname,smark) VALUES (%s,%s)", (name, marks))
            db.commit()
            cur.close()
            return redirect(url_for('detail'))
        if request.form["btn"] == "logout":
            print("AALa")
            session["username"] = ""
            print(session)
            return redirect(url_for('login'))
    print("Up2")
    return render_template("detailsdb.html")


if __name__ == '__main__':
    app.run(debug=True)