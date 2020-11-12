from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from ghettobird import fly
import json
from selenium import webdriver
from pprint import pprint
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=["POST", "GET"])
def main():
    routine = request.json
    options = None
    browser = None
    if "options" in routine.keys():
        options = routine["options"]
        if "browser" in options.keys():
            if options["browser"] == True:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                options["browser"] = browser
    result = fly(routine)
    if browser:
        browser.quit()
    return jsonify(result["results"])

if __name__ == '__main__':
    app.run()

# export FLASK_APP=main.py
