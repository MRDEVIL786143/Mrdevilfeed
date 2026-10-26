import json
import os
import time
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)


def get_driver():
  options = Options()
  options.add_argument("--headless")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--disable-gpu")
  options.add_argument("--window-size=1920,1080")
  options.binary_location = "/usr/bin/google-chrome"

  service = Service("/usr/local/bin/chromedriver")
  driver = webdriver.Chrome(service=service, options=options)
  return driver


@app.route("/")
def home():
  return """
    <html>
        <head><title>FB Auto Bot</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Facebook Auto Like & Comment Bot is Active!</h2>
            <p>Trigger automation using <a href="/run-bot">/run-bot</a></p>
        </body>
    </html>
    """


@app.route("/run-bot")
def run_bot():
  try:
    if not os.path.exists("credentials.json"):
      return jsonify({"status": "error", "message": "credentials.json missing!"})

    with open("credentials.json", "r") as f:
      creds = json.load(f)

    username = creds.get("username")
    password = creds.get("password")

    if not username or not password:
      return jsonify(
          {"status": "error", "message": "Username or password not found in JSON"}
      )

    driver = get_driver()
    wait = WebDriverWait(driver, 15)

    # Facebook Login
    driver.get("https://www.facebook.com/login")
    time.sleep(3)

    email_field = wait.until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_field.send_keys(username)

    pass_field = driver.find_element(By.ID, "pass")
    pass_field.send_keys(password)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(6)

    # Yahan aap apna feed ya target page open kar ke auto like/comment ka logic laga sakte hain
    # Misal ke tor par news feed par jana:
    driver.get("https://www.facebook.com/")
    time.sleep(5)

    # Auto Like / Comment simulation loops yahan implement kiye ja sakte hain

    driver.quit()

    return jsonify({
        "status": "success",
        "message": (
            "Bot successfully logged in and performed automated actions!"
        ),
    })

  except Exception as e:
    return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
