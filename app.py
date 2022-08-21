from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #configuring database location; /// is relative path, //// is absolute
db = SQLAlchemy(app) #database-program connection

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    all_entries = ToDo.query.all() #query to get all entries
    return render_template('index.html', todo_display=all_entries) #todo_display - iterable in index.html

@app.route('/add', methods = ["POST"]) #only when HTML method is POST
def add():
    #getting data from form submission --- <input type="text" name="title" placeholder="Enter to-do">
    new_entry = request.form.get("title") #name = "title" in text-input of form
    new_todo = ToDo(title=new_entry) #didnt have to assign values to id(since primary key), status(has default value); title is a field in ToDo Model
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))  #url_for gives url tied to specific function


#this part of code is reached when hyperlink is clicked
#value after /update/ gets assigned to variable todo_id of integer type

@app.route("/update/<int:todo_id>")
def update(todo_id): #todo_id sent as parameter 
    todo = ToDo.query.filter_by(id=todo_id) #query based on condition
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for("index"))      

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))          

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)    
    