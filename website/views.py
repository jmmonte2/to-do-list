from flask import Blueprint, render_template, request
from werkzeug.utils import redirect
from . import db
from . models import CompletedItems, ToDoItems
from flask_login import current_user


views = Blueprint('views', __name__)



@views.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form['task']
        if task == "":
            tasks = ToDoItems.query.filter_by(user_id=current_user.id)
            print(tasks)
            if tasks == None:
                return render_template("home.html", task_empty=True)
            else:
                return render_template("home.html", task_empty=True, tasks=tasks)
            
        else:
            new_task =  ToDoItems(item_info=task, user_id=current_user.id)  #create todo object

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/home")
        except:
            return "Issuing adding Task"


    else:
        tasks = ToDoItems.query.filter_by(user_id=current_user.id)
        task_count = ToDoItems.query.filter_by(user_id=current_user.id).count()
        completed_count = CompletedItems.query.filter_by(user_id=current_user.id).count()
        return render_template("home.html",tasks=tasks, task_count=task_count, completed_count=completed_count)


@views.route('/delete/<int:id>')
def delete_task(id):
    task_deleted = ToDoItems.query.get_or_404(id)
    task_completed =  CompletedItems(user_id=current_user.id)
    try:
        db.session.add(task_completed)
        db.session.commit()
        db.session.delete(task_deleted)
        db.session.commit()
        return redirect('/home')
    except:
        return 'Issue deleting task'


@views.route('update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = ToDoItems.query.get_or_404(id)
    if request.method == 'POST':
        task.item_info = request.form['task']
        if task.item_info == "":
            return render_template("update.html", task=task, task_empty=True)

        try:
            db.session.commit()
            return redirect('/home')
        except:
            return "issue making update"
        
    else:
        return render_template("update.html", task=task)