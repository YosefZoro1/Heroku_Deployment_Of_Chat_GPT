#from cs50 import SQL
from flask import Flask, render_template, request
# from flask_session import Session
import openai, os
# from dotenv import load_dotenv

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# this route takes you to the index (main) page to input the question
# it will forward the prompt through the action form to answer.html 

@app.route("/")
def mainroute():
    return render_template("index.html")

@app.route('/chatgpt', methods=['GET'])
def open_ai():
  domains_data[0]["visits"] += 1
  text = request.args.get('query', '')
  key = 'darkman|YVg3cyukPe8jSVBb8VuLT3BlbkFJlh0mhBk714FLEBOobPN1'
  i = (key).split('darkman|')[1]
  openai.api_key = f'sk-{i}'
  try:
    if text == '':
      return Not_text()

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "user",
                                                  "content": text
                                              }])
    answer = completion.choices[0].message["content"]
    return jsonify({"result": answer})
  except Exception as e:
    return jsonify({
        'error': str(e),
        'result': 'An internal server error occurred'
    }), 500
)        
    

