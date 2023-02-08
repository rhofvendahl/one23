from flask import Flask, send_from_directory
from flask_restful import Api
from api.ConversationHandler import ConversationHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')

api = Api(app)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

api.add_resource(ConversationHandler, "/conversation")

if __name__ == "__main__":
    app.run()
