from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MONGO_DBNAME'] = 'Homework2'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Homework2'

mongo = PyMongo(app)

@app.route('/')
def profile():
    if 'username' in session:
        users = mongo.db.users
        login_users = users.find_one({'name' : session['username']})

        img_source = ""
        if login_users['Gender'] == "Male":
            img_source = "static/male.jpg"
        elif login_users['Gender'] == "Female":
            img_source = "static/female.jpg"
        else:
            img_source = "static/other.png"

        return render_template('Profile.html',
                                fname = login_users['FirstName'],
                                sname = login_users['SecondName'],
                                tname = login_users['ThirdName'], 
                                birth = login_users['Birthday'], 
                                field = login_users['FOI'], 
                                gender = login_users['Gender'],
                                img = img_source)

    return render_template('Login.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    users = mongo.db.users
    login_users = users.find_one({'name' : request.form['uname']})
    if login_users:
        if request.form['psw'] == login_users['password']:
            session['username'] = request.form['uname']
            return redirect(url_for('profile'))
        return render_template('Login.html',error="Invalid Username/Password")
    return render_template('Login.html',error="Invalid Username/Password Combination")

    return render_template("Login.html")

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            if request.form['psw'] == request.form['cpsw']:
                hashpass = request.form['psw']
                users.insert_one( {'name' : request.form['username'], 'password' : hashpass,
                'FirstName' : request.form['fname'], 'SecondName' : request.form['ffname'],
                'ThirdName' : request.form['tname'], 'Birthday' : request.form['birthday'],
                'FOI' : request.form['field'], 'Gender' : request.form['gender']} )
                session['username'] = request.form['username']

                if request.form['blogged']:
                    blog = mongo.db.blogs
                    blog.insert_one({'name' : request.form['fname']+""+request.form['tname'] , 'Blog' : request.form['blogged']})
                return redirect(url_for('profile'))
            return render_template('SignUp.html',error="Please Enter Same password")
        return render_template('SignUp.html',error="That Username Exists")
    
    return render_template('SignUp.html')



@app.route('/blog', methods = ['POST','GET'])
def blog():
    if 'username' in session:
        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : session['username']})
            name = existing_user['FirstName'] 
            blogs = mongo.db.blogs
            blogs.insert_one(
                {'name' : name , 'Blog' : request.form['blogged']}
            )
            return render_template('Blog.html')
        return render_template(url_for('profile'))
    return render_template('Blog.html')


@app.route('/logout')
def logOut():
    session.pop('username',None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host = "localhost",port =5000,debug = True)