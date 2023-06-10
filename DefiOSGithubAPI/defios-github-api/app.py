from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from github import AppAuthentication
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

app_id = int(config["github"]["app_id"])
cert_path = config["github"]["cert_path"]
# Read the bot certificate
with open(cert_path, "r") as cert_file:
    app_key = cert_file.read()


class PingLive(Resource):
    def get(self):
        return "Alive"


class GithubWebhook(Resource):
    def post(self):
        payload = request.json
        logging.info(payload)
        github_app = AppAuthentication(
            app_id=app_id,
            private_key=app_key,
            installation_id=payload["installation"]["id"],
        )
        if "issue" in payload.keys() and payload["action"] == "opened":
            create_issue_comment(
                github_app, payload, "../markdown_files/issue_opened.md"
            )
            return "Done"
        if "issue" in payload.keys() and payload["action"] == "closed":
            create_issue_comment(
                github_app, payload, "../markdown_files/issue_closed.md"
            )
            return "Done"
        if "pull_request" in payload.keys() and payload["action"] == "opened":
            create_pr_comment(
                github_app, payload, "../markdown_files/pull_request_opened.md"
            )
            return "Done"
        if "pull_request" in payload.keys() and payload["action"] == "closed":
            create_pr_comment(
                github_app, payload, "../markdown_files/pull_request_closed.md"
            )
            return "Done"


api.add_resource(PingLive, "/health")
api.add_resource(GithubWebhook, "/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
