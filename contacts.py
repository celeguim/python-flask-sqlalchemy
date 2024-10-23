import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contacts.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        contact = Contact(name=request.form.get("name"))
        contact.phone = request.form.get("phone")
        db.session.add(contact)
        db.session.commit()
    contacts = Contact.query.all()
    return render_template("home.html", contacts=contacts)

@app.route("/update", methods=["POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    newphone = request.form.get("newphone")
    oldphone = request.form.get("oldphone")
    contact = Contact.query.filter_by(name=oldname).first()
    contact.name = newname
    contact.phone = newphone
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    contact = Contact.query.filter_by(name=name).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect("/")

class Contact(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return "<Name: {} - Phone: {}>".format(self.name, self.phone)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
