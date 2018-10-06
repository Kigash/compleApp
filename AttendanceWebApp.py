from flask import Flask,request,render_template,redirect,url_for,session,flash,json
from lecture import *
from user import *

app = Flask(__name__)
app.secret_key = "yohanamtembeziiukjyhgfdsfghlkjhgfdsx1234567jkhgfdsfghj"

@app.route('/new-lecture')
def newProject():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('lecture_form.html')


@app.route('/edit/<int:id>')
def edit(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    # try:
    user_id=session.get("id")
    print('my session', user_id)
    lecture = Lecture.get(Lecture.id==id,Lecture.user_id==user_id)
        # lec = Lecture.select().where(Lecture.id == id)
    #print('my lec',lecture)
    return render_template("edit.html",lecture=lecture)

    # except:
    #     flash("could not find this lecture")
    #     return redirect(url_for("lectures"))

@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")

#@app.route('/home')
#def home():
    #return render_template("home.html")

@app.route("/jsonData")
def jsonData():
    person={"name":"Kiganya","location":"Nairobi","work":"Surestep"}
    
    return json.dumps(person)


@app.route('/register')
def register():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user_id = session.get("id")
    try:
        user = User.get(User.id==user_id)
        if user.role == 'admin':
            return render_template("register.html")
        else:
            return 'ERROR!!! Contact the Admin(YOHANAMTEMBEZI.com) to view this page'
    except:
        return 'ERROR!!! Contact the Admin(YOHANAMTEMBEZI.com) to view this page'


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/add-user',methods=["POST"])
def add_user():
    if request.method == "POST":
        names =request.form['names']
        reg_no =request.form['reg_no']
        dob = request.form['dob']
        email = User.get(User.email == request.form['email']).email
            #if email:
                #flash('User alredy Exists')
                #return  render_template('login.html')
        course= request.form['course']
        department= request.form['department']
        phone_no= request.form['phone_no']
        address= request.form['address']
        password = request.form['password']
        role = request.form['role']
        User.create(names=names,email=email,role=role,address=address,phone_no=phone_no,department=department,course=course,password=password,reg_no=reg_no,dob=dob)
    return redirect(url_for('login'))

@app.route('/signin',methods = ["POST"])
def signin():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        x = User.get(User.email == email, User.password == password)

        if(x ==email, x ==password):
            session["names"]= x.names
            session["id"]= x.id
            session["logged_in"]= True
            #print(email)
            flash('loged in')
            return redirect(url_for("newProject"))
        else:
            #if session["logged_in"] = False :
            flash("wrong username or password")
            return render_template('login.html')
        #User.signin(email=email,password=password)
    #return redirect(url_for('login'))

@app.route('/save/<int:id>',methods=['POST'])
def save(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user_id = session.get("id")
    try:
        lecture = Lecture.get(Lecture.id==id,Lecture.user_id==user_id)
        if request.method=="POST":
            lecture.course=request.form['course']
            lecture.unit = request.form['unit']
            lecture.unit_code = request.form['unit_code']
            lecture.start_time = request.form['start_time']
            lecture.end_time = request.form['end_time']
            lecture.date = request.form['date']
            lecture.department= request.form['department']
            lecture.lecturer= request.form['lecturer']
            lecture.save()
            flash("lecture edited successfully")
    except:
        flash("Could not edit Lecture")
    return redirect(url_for("lectures"))

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    try:
        user_id=session.get("id")
        lecture = Lecture.get(Lecture.id==id,Lecture.user_id==user_id)
        lecture.delete_instance()
        flash("lecture deleted successfully")
    except:
        flash("could not delete the lecture")
    return redirect(url_for("lectures"))

@app.route('/lectures')
def lectures():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user_id= session.get("id")
    lectures= Lecture.select().where(Lecture.user_id==user_id)
    return render_template('lectures.html', lectures=lectures)

@app.route('/add', methods=["post"])
def add():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method=="POST":
        course=request.form['course']
        unit = request.form['unit']
        unit_code = request.form['unit_code']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        date = request.form['date']
        department = request.form['department']
        lecturer = request.form['lecturer']
        user_id=session.get("id")
        Lecture.create(course=course,unit=unit,unit_code=unit_code,start_time=start_time,end_time=end_time,date=date,department=department,lecturer=lecturer,user_id=user_id)
        flash("Lecture was saved successfully")
    return redirect(url_for("lectures"))

# Admin Routes

def loginCheck():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user_id = session.get("id")
    try:
        user = User.get(User.id==user_id)
        if user.role == 'admin':
            return 1
        else:
            return 0
    except:
        return 'ERROR!!! Contact the Admin(admin@admin.com) to view this page'

@app.route('/admin/lectures')
def admin():
    if loginCheck() == 1:
        lectures = Lecture.select()
        return render_template('admin/lectures.html', lectures=lectures)
    else:
        return 'ERROR!!! Contact the Admin(admin@admin.com) to view this page'



if __name__ == '__main__':
    app.run(debug='true')
