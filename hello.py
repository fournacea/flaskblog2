#Import statements
from flask import (
    Flask,
    flash, 
    make_response,
    render_template, 
    redirect,
    request, 
    url_for, 
    )
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin, 
    login_user, 
    logout_user,
    login_required,
    LoginManager,
    current_user,
    )
from webforms import(
    LoginForm,
    NamerForm,
    PasswordForm,
    PostForm,
    SearchForm,
    UserForm,
    )  
from flask_ckeditor import CKEditor


    #Initialize and Configure the App
#--------------------------------------
    #Create a Flask Instance
app = Flask(__name__)

    #Initialize CKEditor
ckeditor = CKEditor(app)

    #Add Database
    #Old SQLite Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.app_context().push()
    
    #New MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
app.app_context().push()
    #Create a Secret Key
app.config['SECRET_KEY'] = "SuperDuper-Secret-Key"

    #Initialize the Database
db = SQLAlchemy(app)
    #Migrate the Database
migrate = Migrate(app, db)

    #Flask Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


    #Create Route Decorators
#--------------------------------------------------------------------------------

    #Pass Stuff To Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


   #Homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
        title=form.title.data,
        content = form.content.data,
        poster_id=poster,
        slug = form.slug.data
        )
        #Clear the Form
        form.title.data = ""
        form.content.data = ""
        #form.author.data = ""
        form.slug.data = ""
            #Add Post Data to the Database
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Submitted! Success!")
    return render_template("add_post.html", form=form)


   #Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 42:
        return render_template("admin.html")
    else:
        flash("Sorry, You Must Be An Admin To Access The Admin Page...")
        return redirect(url_for('dashboard'))
 
    
    #Create Dashboard Route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


    #Create Delete Route
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    our_users = Users.query.all()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Success! User was Deleted")
        return redirect(url_for('add_user'))
        
    except:
        flash("Whoops! There was a problem deleting user. Please try again!")
        return render_template(
        "add_user.html",
        form=form,
        name=name,
        our_users=our_users
        )


    #Create Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
                #Check the Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successful!')
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password! Please Try Again")
        else:
            flash("This User Doesn't Exist! Please Try Again")
    return render_template('login.html', form=form)


    #Create Logout Route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! See You Again Soon!")
    return redirect(url_for('login'))


    #Create a Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
        #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form was succesfully submitted.")
    return render_template(
        "name.html", 
        name=name, 
        form=form
        )


    #Create Delete Posts Route
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
                #Grab all the Posts from the Database
            posts = Posts.query.order_by(Posts.date_posted)
            flash("Blog Post was Deleted!")
            return render_template("posts.html", posts=posts)
            
        except:
                #Grab all the Posts from the Database
            posts = Posts.query.order_by(Posts.date_posted)
            flash("There Was a Problem Deleting the Post. Please Try Again!")
            return render_template("posts.html", posts=posts)
    else:
            #Grab all the Posts from the Database
        posts = Posts.query.order_by(Posts.date_posted)
        flash("You Are Not Authorized To Delete That Post!")
        return render_template("posts.html", posts=posts)


@app.route('/posts')
def posts():
        #Grab all the Posts from the Database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
        #Grab Post from the Database Matching the ID
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
        #Grab all the Posts from the Database
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit(): #If Validated, Place Form Data in Variables
        post.title = form.title.data
        #post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
            #Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post has been Succesfully Updated!")
        return redirect(url_for('post', id=post.id))
    
    if current_user.id == post.poster.id:
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You Are Not Authorized To Edit That Post!")
        return redirect(url_for('posts', posts=posts))


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
            #Get Data From Submitted Form
        post.searched = form.searched.data
            #Query The Database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template(
            "search.html",
             form=form,
             searched=post.searched,
             posts=posts
             )


    #Update Database Records
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST': #Submit via POST
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.about_author = request.form['about_author']
        try: #Try to Commit to Database
            db.session.commit()
            flash("User Updated!")
            return redirect(url_for('add_user'))
            #return render_template("update.html",
            #form=form, 
            #name_to_update=name_to_update,
            #id=id)
        except: #Database Operation Failure
            flash("Error! There was a problem submitting data")
            return render_template(
            "update.html", 
            form=form, 
            name_to_update=name_to_update, 
            id=id
            )
    else: #Submit via GET
        return render_template(
        "update.html", 
        form=form, 
        name_to_update=name_to_update, 
        id=id
        )


#Create Add User Route
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None #Initialize name Variable
    form = UserForm() #Create flask-WTF Form
    if form.validate_on_submit():#If TRUE grab first matching email from DB
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: #If no user then create one
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(
            name=form.name.data,
            username = form.username.data,
            email=form.email.data, 
            favorite_color=form.favorite_color.data,
            about_author=form.about_author.data,
            password_hash = hashed_pw
            )
                #Add and Commit to Database
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""  #Reset name 
        form.username.data = ""  #Reset username
        form.email.data = "" #Reset email
        form.favorite_color.data = "" #Reset favorite_color
        form.about_author.data = "" #Reset about_author
        form.password_hash.data = "" #Reset password_hash
        flash("Form was successfully submitted")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
    form=form,
    name=name,
    our_users=our_users)


    #Echo Username Page
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)
    #return "<h1>Hello, {}!</h1>".format(name)


    #Create a Test Password Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
        #Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
            #Clear the Form
        form.email.data = ""
        form.password_hash.data = ""
            #Lookup User by Email Address
        pw_to_check = Users.query.filter_by(email=email).first()
        if pw_to_check is None:
            flash("Email address not found!")
            return redirect(url_for("test_pw"))
        else:
                #Check Hashed Password
            passed = check_password_hash(pw_to_check.password_hash, password)
            flash("Checking password hash...")
    return render_template(
        "test_pw.html", 
        email=email, 
        password=password,
        pw_to_check=pw_to_check,
        passed=passed, 
        form=form
        )


@app.route('/teapot')
def teapot():
    response = make_response(render_template("teapot.html"))
    response.status_code = 418
    return response


    #JSON APIs
#--------------------------------------------------------
    #JSON "API"
@app.route('/date')
def get_current_date():
   return {"Date": date.today()}


    #JSON "API"
@app.route('/fav_pizza')
def fav_pizza():
    favorite_pizza = {
        "John": "Pepperoni",
        "Mike": "Pineapple",
        "Sarah": "Cheese",
        "Leah" : "Mushroom",
        }
    return favorite_pizza


    #Error Pages Route Decorators
#----------------------------
    #Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


    #Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


    #I'm a Little Teapot
@app.errorhandler(418)
def teapot(e):
    return render_template("teapot.html"), 418


    #Database Models
#-------------------------------------------------------------------
    #Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
        #Password Stuff!
    password_hash = db.Column(db.String(128))
    #Users Can Have Many Posts
    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError('password is not a readable atrribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Name %r>" % self.name 

    #Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255)) 
    content = db.Column(db.Text) 
    #author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug =  db.Column(db.String(255)) 
    #Foreign Key to Link Users(refer to primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Dunder Main
#----------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
