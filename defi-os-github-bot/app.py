from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, request
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

class PingLive(Resource):
    def get():
        return "Alive"
    
api.add_resource(PingLive,"/health")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)