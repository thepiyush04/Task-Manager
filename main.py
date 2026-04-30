from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.secret_key = 'mnc_secure_key_2026' # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================
# DATABASE MODELS (Schema)
# ==========================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False) # 'Admin' or 'Member'
    tasks = db.relationship('Task', backref='assignee', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Done
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# ==========================================
# SECURITY DECORATORS
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'Admin':
            flash("Admin access required.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# ROUTES (APIs)
# ==========================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'] # Admin or Member
        
        # Security: Hash the password before saving
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    if session['role'] == 'Admin':
        # Admin sees everything
        projects = Project.query.all()
        users = User.query.filter_by(role='Member').all()
        tasks = Task.query.all()
    else:
        # Members only see their tasks
        projects = []
        users = []
        tasks = Task.query.filter_by(user_id=session['user_id']).all()
        
    return render_template('dashboard.html', projects=projects, users=users, tasks=tasks)

@app.route('/create_project', methods=['POST'])
@login_required
@admin_required
def create_project():
    name = request.form['name']
    new_proj = Project(name=name)
    db.session.add(new_proj)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/create_task', methods=['POST'])
@login_required
@admin_required
def create_task():
    title = request.form['title']
    project_id = request.form['project_id']
    user_id = request.form['user_id']
    
    new_task = Task(title=title, project_id=project_id, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    # Ensure members can only update their own tasks
    if session['role'] == 'Member' and task.user_id != session['user_id']:
        return "Unauthorized", 403
        
    task.status = request.form['status']
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)