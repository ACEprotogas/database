from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sungodnika'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.before_request   
def create_tables():
    db.create_all()    


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Update existing user
            existing_user.name = name
            existing_user.phone = phone
            db.session.commit()
            flash('User information updated successfully!', 'success')
        else:
            new_user = User(name=name, email=email, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            flash('New user added successfully!', 'success')

        return redirect (url_for('show'))
    
    return render_template('index.html')

@app.route('/show')
def show():
    users= User.query.all()
    return render_template('show.html', users=users)


if __name__ == "__main__":
    app.run()(debug=True)

