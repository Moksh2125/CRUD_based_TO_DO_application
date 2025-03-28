from flask import Flask, render_template, redirect , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_scss import Scss
# My app setup
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Data Class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = True)
    complete = db.Column(db.Integer, default = 0)

    created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
    db.create_all()

@app.route("/", methods = ['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        current_task = request.form["content"]  # Uses the ID of the input field
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR : {e}")
            return f"ERROR : {e}"
    # see all the current task
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks = tasks)

@app.route("/delete/<int:id>")
def delete(id : int):
    task__delete = MyTask.query.get_or_404(id)
    try :
        db.session.delete(task__delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:    
        print(f"ERROR : {e}")  
        return f"ERROR : {e}" 

@app.route("/update/<int:id>", methods = ['POST', 'GET'])
def update(id : int):
    task  = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR : {e}")
            return f"ERROR : {e}"
    else:
            return render_template("update.html", task = task)


if __name__ == "__main__" :
    

    app.run(debug = True)