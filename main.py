from flask import Flask, request, jsonify
from ghettobird import fly
import json
from selenium import webdriver
from pprint import pprint

app = Flask(__name__)


@app.route('/', methods=["POST"])
def main():
    routine = request.json
    options = None
    browser = None
    if "options" in routine.keys():
        options = routine["options"]
        if "browser" in options.keys():
            if options["browser"] == True:
                chromedriver_location = 'c:/chromedriver.exe'
                options["browser"] = webdriver.Chrome(
                    executable_path=chromedriver_location)
    result = fly(routine)
    if browser:
        browser.quit()
    return jsonify(result["results"])


if __name__ == '__main__':
    app.run()

# export FLASK_APP=main.py
