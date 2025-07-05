from flask import Flask, request, render_template, redirect
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

@app.route("/")
def about_page():
    return render_template("about.html", thank_you=False)

@app.route("/send", methods=["POST"])
def send_email():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    email_message = f"Subject: New Contact from {name} ({email})\n\n{message}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message)
        return "Message sent successfully!"
    except Exception as e:
        return f"Error: {e}"
