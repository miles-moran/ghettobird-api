from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from ghettobird import fly
import json
from selenium import webdriver
from pprint import pprint
import os
from database import db
from pprint import pprint

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def getBlueprintById(id, docs):
    for doc in docs:
        if doc.id == id:
            return doc

def runRoutine(routine):
    pprint(routine)
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
    try:
        result = fly(routine)
    except Exception as e:
        print('-------------------------------------------')
        print(e)
        print('-------------------------------------------')
    if browser:
        browser.quit()
    return routine

@app.route('/api', methods=["GET"])
def getBlueprint():
    gid = request.args.get('gid')
    blueprints_ref = db.collection('blueprints')
    docs = blueprints_ref.stream()
    blueprint = getBlueprintById(gid, docs).to_dict()
    scraped = runRoutine(blueprint["blue"])
    return jsonify(scraped["results"])

@app.route('/', methods=["POST", "GET"])
def main():
    routine = request.json
    scraped = runRoutine(routine)
    return jsonify(scraped["results"])

if __name__ == '__main__':
    app.run()

# export FLASK_APP=main.py
