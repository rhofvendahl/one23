from flask import jsonify
from flask_restful import Resource, reqparse
import os
import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

parser = reqparse.RequestParser()
parser.add_argument("password")
parser.add_argument("conversation")
parser.add_argument("userInput")

class ConversationHandler(Resource):
    
    def post(self):
        try:
            request_data = parser.parse_args()

            password = request_data["password"]

            if password != os.getenv("PASSWORD"):
                return jsonify({
                    "passwordCorrect": False,
                })

            if "conversation" not in request_data:
                return jsonify({
                    "passwordCorrect": True,
                })

            conversation = request_data["conversation"]

            user_input = request_data["userInput"].strip()

            mod = openai.Moderation.create(
                input=user_input
            )

            user_ws = "\n" if "\n" in user_input else " " 
            
            if conversation == "":
                conversation = f"User:{user_ws}{user_input}\n\nAI:"
            else:
                conversation = conversation + "\n\nUser: " + user_input + "\n\nAI:"
                
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=conversation,
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["User:"],
            )

            response_text = response["choices"][0]["text"].strip()

            response_ws = "\n" if "\n" in response_text else " " 

            conversation = f"{conversation}{response_ws}{response_text}"
        
            return jsonify({
                "passwordCorrect": True,
                "conversation": conversation,
                "moderation": mod["results"][0],
            })  
        except Exception as err:
            print(err)
            return "", 500

