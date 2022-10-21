from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, TextAreaField
from wtforms.validators import DataRequired
import smtplib
import os

my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    message = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Send Message")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/connect', methods=["GET", "POST"])
def connect():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="aumbattul99@gmail.com",
                msg=f"Subject:Someone wants to contact you.."
                    f"\n\nName: {name}"
                    f"\n\nEmail: {email}"
                    f"\n\nMessage: {message}"
            )
            form.name.data = ""
            form.email.data = ""
            form.message.data = ""
            return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)