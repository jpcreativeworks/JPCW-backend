from flask import Flask, request, render_template, redirect, url_for
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage


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
    
    confirmation = EmailMessage()
    confirmation["Subject"] = "JP Creative Works received your message!"
    confirmation["From"] = EMAIL_ADDRESS
    confirmation["To"] = email
    confirmation.set_content(f"Hi {name}, thanks for your message!")  # fallback
    confirmation.add_alternative(f"""\
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Hi {name},</p>
        <p>Thank you for reaching out to <strong>JP Creative Works</strong>. Your message has been received, and we'll get back to you as soon as possible.</p>
        <p><strong>Here's what you sent:</strong><br>
        <em>{message}</em></p>
        <p>In the meantime, feel free to follow us on 
          <a href="https://www.instagram.com/jpcreativeworks" target="_blank">@jpcreativeworks</a> 
          or visit our site again at 
          <a href="https://jpcreativeworks.netlify.app" target="_blank">jpcreativeworks.netlify.app</a>.
        </p>
        <p>Thanks again for reaching out! I’m excited to connect and collaborate with you.</br>
        – Jenn Bencriscutto<br>
        JP Creative Works</p>
      </body>
    </html>
    """, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message)
            smtp.send_message(confirmation)  # <-- This sends the HTML version
        return redirect(url_for("contact_iframe", success="true"))
    except Exception as e:
        return f"Error: {e}"
      
@app.route("/contact-iframe")
def contact_iframe():
    return render_template("contact-form.html")
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or fallback to 5000
    app.run(host="0.0.0.0", port=port)
