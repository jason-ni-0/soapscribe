import os
import openai
from flask import Flask, render_template, request, redirect, url_for, session
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.config.from_object(Config)
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'diagnosis' in request.form:
        diagnosis = request.form["diagnosis"]
        sympResponse = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"lowercase comma delimited list of the symptoms of {diagnosis}",
            temperature=0.7,
            max_tokens=714,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        symptom = sympResponse["choices"][0]["text"]
        treatmedResponse = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Go in depth in a paragraph on the medical treatments(specific names and brands) of {diagnosis} in sentences.",
            temperature=0.7,
            max_tokens=714,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        treathomeResponse = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Go in depth in a paragraph on the home treatments of {diagnosis} in sentences.",
            temperature=0.7,
            max_tokens=714,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        medTreat = treatmedResponse["choices"][0]["text"]
        homeTreat = treathomeResponse["choices"][0]["text"]
        planResponse = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"How to prevent {diagnosis} (lowercase comma delimited list) and how long(specific time) after doctor visit should patient return to doctor office?",
            temperature=0.7,
            max_tokens=714,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        plan = planResponse["choices"][0]["text"]
        return render_template('home.html', diagnosis=diagnosis, symptoms=symptom, medTreat=medTreat, homeTreat=homeTreat, plan=plan)
    return render_template('home.html')

if __name__ == "__main__":
    app.run()