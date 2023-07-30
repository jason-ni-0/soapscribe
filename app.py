import os
import openai
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

app = Flask(__name__)
# app.config.from_object(Config)
PORT = os.environ.get('PORT')
openai.api_key = os.environ.get('OPENAI_API_KEY')

def getSymptoms(diagnosis, res):
    sympResponse = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"lowercase comma delimited list of the symptoms of {diagnosis}",
        temperature=0.7,
        max_tokens=714,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res[0] = sympResponse

def getMedTreatments(diagnosis, res):
    treatmedResponse = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Go in depth in a paragraph on the medical treatments(specific names and brands) of {diagnosis} in sentences, then go in depth in a separate paragraph on the home treatments of {diagnosis} in sentences.",
        temperature=0.7,
        max_tokens=714,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res[0] = treatmedResponse

def getPlan(diagnosis, res):
    planResponse = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"How to prevent {diagnosis} (lowercase comma delimited list) and how long(specific time) after doctor visit should patient return to doctor office?",
        temperature=0.7,
        max_tokens=714,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res[0] = planResponse

@app.route('/api/v1/health', methods=['GET'])
def health():
    return {'message':'OK'}

@app.route('/api/v1/generate', methods=['GET', 'POST'])
def home():
    if 'diagnosis' in request.args:
        diagnosis = request.args["diagnosis"]

        # create return variables for symptoms, treatments, and plan
        sympResponse = [None]
        treatmedResponse = [None]
        planResponse = [None]

        # create threads for symptoms, treatments, and plan
        sympThread = threading.Thread(target=getSymptoms, args=(diagnosis, sympResponse))
        treatThread = threading.Thread(target=getMedTreatments, args=(diagnosis, treatmedResponse))
        planThread = threading.Thread(target=getPlan, args=(diagnosis, planResponse))

        # start threads and wait for all completion
        sympThread.start()
        treatThread.start()
        planThread.start()
        sympThread.join()
        treatThread.join()
        planThread.join()
        
        symptom = sympResponse[0]["choices"][0]["text"]
        medTreat = treatmedResponse[0]["choices"][0]["text"]
        plan = planResponse[0]["choices"][0]["text"]

        return {'diagnosis': diagnosis, 'symptoms':symptom, 'medTreat': medTreat, 'plan': plan}
    return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)