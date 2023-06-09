from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from github import GithubIntegration
from helpers import create_issue_comment, create_pr_comment
import configparser
import logging

# configuring logging datetime and file configuration
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filename="app.log",
    level=logging.INFO,
)

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

config = configparser.ConfigParser()
config.read("config.ini")

app_id = config["github"]["app_id"]
cert_path = config["github"]["cert_path"]
# Read the bot certificate
with open(cert_path, "r") as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


class PingLive(Resource):
    def get(self):
        return "Alive"


class GithubWebhook(Resource):
    def post(self):
        payload = request.json
        logging.info(payload)
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
            create_pr_comment(
                git_integration, payload, "../markdown_files/pull_request_opened.md"
            )
            return "Done"


api.add_resource(PingLive, "/health")
api.add_resource(GithubWebhook, "/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
