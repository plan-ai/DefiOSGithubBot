from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from github import GithubIntegration
from helpers import create_issue_comment
import configparser

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

config = configparser.ConfigParser()
config.read("config.ini")

app_id = config["github"]["app_id"]
cert_path = config["github"]["cert_path"]
# Read the bot certificate
with open("r", cert_path) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


class PingLive(Resource):
    def get():
        return "Alive"


class GithubWebhook(Resource):
    def post():
        payload = request.json()
        if "issue" in payload.keys() and payload["action"] == "opened":
            create_issue_comment(
                git_integration, payload, "../markdown_files/issue_opened.md"
            )
            return "Done"
        if (
            "issue" in payload.keys()
            and payload["action"] == "closed"
            and payload["issue"]["active_lock_reason"] == "resolved"
            and "pull_request" in payload["issue"].keys()
        ):
            create_issue_comment(
                git_integration, payload, "../markdown_files/issue_closed.md"
            )
            return "Done"
        if "pull_request" in payload.keys() and payload["action"] == "opened":
            create_issue_comment(
                git_integration, payload, "../markdown_files/issue_closed.md"
            )
            return "Done"


api.add_resource(PingLive, "/health")
api.add_resource(GithubWebhook, "/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
