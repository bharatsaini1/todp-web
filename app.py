from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TODO-list.db'

db = SQLAlchemy(app)

class TODO(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    desc  = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default =datetime.utcnow )

    def __repr__(self):
        return  f"{self.sno} - {self.Title}"


@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        Title = request.form['Title']
        desc = request.form['desc']

        todo = TODO(Title=Title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = TODO.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/Update/<int:sno>",methods=['GET', 'POST'])
def Update(sno):
    if request.method == 'POST':
        Title = request.form['Title']
        desc = request.form['desc']
        todo = TODO.query.filter_by(sno=sno).first()
        todo.title = Title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = TODO.query.filter_by(sno=sno).first()
    return render_template('Update.html', todo=todo)
    

@app.route("/Delete/<int:sno>")
def Delete(sno):
    todo = TODO.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/about")
def  about():
    return render_template('about.html')





if __name__ == '__main__':
    app.run(debug=True)
