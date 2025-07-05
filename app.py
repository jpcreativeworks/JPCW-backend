from flask import Flask, request, render_template, redirect, url_for
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
        return redirect(url_for("contact_iframe", success="true"))
    except Exception as e:
        return f"Error: {e}"
      
@app.route("/contact-iframe")
def contact_iframe():
    return render_template("contact-form.html")
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or fallback to 5000
    app.run(host="0.0.0.0", port=port)
