# Task Management System

Hey there! Welcome to my project. I built this full-stack Task Management System as part of my assignment to demonstrate how web applications handle real-world business logic, specifically focusing on user permissions and data isolation.

## 💡 The Goal Behind This Project
I wanted to build something practical. Most basic to-do apps are single-user, but in a real company, tasks are delegated. So, my main focus was figuring out how to implement **Role-Based Access Control (RBAC)** from scratch. I wanted to see how a system handles a Manager assigning a task, and an Employee executing it.

## 🚀 What It Actually Does

* **Two-Tier System:** The app recognizes who is logging in. 
* **Admin Dashboard:** If you log in as an Admin, you get the master view. You can create projects, break them down into tasks, set deadlines, and assign them directly to specific employees.
* **Employee Dashboard:** If you log in as an Employee, the UI changes. You only see the tasks assigned specifically to you, keeping things distraction-free. You can update your progress (Pending -> In Progress -> Completed).
* **Automated Deadline Tracking:** I wrote custom logic that compares the task deadline with the current server date. If a task is past due and not completed, it automatically gets a red "Overdue" badge. (This was honestly my favorite feature to build!)

## 🛠️ Tech Stack & Why I Chose It

* **Backend:** Python & Flask. I chose Flask because it's lightweight and forced me to understand the routing and logic manually rather than relying on a heavy framework.
* **Database:** SQLite managed via SQLAlchemy ORM.
* **Frontend:** HTML5, CSS3, and Bootstrap. I used the 'Flatly' theme to keep the UI clean and professional without overcomplicating the frontend code.
* **Hosting:** Deployed live on Railway, connected directly to my GitHub for CI/CD.

## 🧠 Challenges & What I Learned
Taking this from localhost to a live cloud environment was a huge learning curve. I ran into issues with database integrity constraints (like preventing duplicate usernames) and learned how free-tier cloud servers handle "sleep states." Figuring out how to securely manage user sessions so an employee can never access the admin route was tricky, but incredibly rewarding once it finally worked.

## 🔗 Live Demo
**Check out the live app here:** [task-manager-production-00fd.up.railway.app]

## 💻 How to Run It Locally

If you want to run the code on your own machine:

1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it and install dependencies: `pip install -r requirements.txt`
4. Run the app: `python main.py`
5. Open `http://127.0.0.1:5000` in your browser.

## 🔑 Testing Credentials

To test the role-based features without creating a new account, you can use these default credentials:

* **Admin Role:**
  * Username: `admin_manager`
  * Password: `admin123`

---
**Designed and coded by Piyush Shukla**
GitHub: [@thepiyush04](https://github.com/thepiyush04)
