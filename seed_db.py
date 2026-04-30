# seed_db.py
from app import app, db, User, Project, Task
from werkzeug.security import generate_password_hash

def seed_database():
    """Populates the database with initial test data for deployment validation."""
    with app.app_context():
        # Clear existing data to prevent duplicates during testing
        db.drop_all()
        db.create_all()

        # 1. Create Users
        admin_user = User(
            username='admin_manager',
            password_hash=generate_password_hash('admin123'),
            role='Admin'
        )
        
        team_member = User(
            username='software_dev_1',
            password_hash=generate_password_hash('dev123'),
            role='Member'
        )
        
        db.session.add_all([admin_user, team_member])
        db.session.commit()

        # 2. Create a Project
        project_alpha = Project(name='Q3 Enterprise Release')
        db.session.add(project_alpha)
        db.session.commit()

        # 3. Create Tasks
        task1 = Task(
            title='Design database schema for new module',
            status='Done',
            project_id=project_alpha.id,
            user_id=team_member.id
        )
        
        task2 = Task(
            title='Implement JWT authentication',
            status='In Progress',
            project_id=project_alpha.id,
            user_id=team_member.id
        )
        
        task3 = Task(
            title='Write unit tests for REST APIs',
            status='Pending',
            project_id=project_alpha.id,
            user_id=team_member.id
        )

        db.session.add_all([task1, task2, task3])
        db.session.commit()

        print("Database successfully seeded with test data.")

if __name__ == '__main__':
    seed_database()
    