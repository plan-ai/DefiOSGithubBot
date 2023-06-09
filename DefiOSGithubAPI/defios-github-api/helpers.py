from github import Github


def get_pull_request_no(payload):
    if " issue" in payload.keys():
        url = payload["issue"]["pull_request"]["url"]
        pull_request_no = url.split("pull/")[1]
    elif "pull_request" in payload.keys():
        pull_request_no = payload["number"]
    return pull_request_no


def get_issue(git_integration, payload):
    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    pull_request_no = get_pull_request_no(payload)
    issue = repo.get_issue(number=pull_request_no)
    return issue

def get_pr(git_integration, payload):
    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    pull_request_no = get_pull_request_no(payload)
    pr = repo.get_pull(number=pull_request_no)
    return pr

def create_comment(issue, comment):
    issue.create_comment(comment)


def read_markdown(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    return text


def create_issue_comment(git_integration, payload, comment_path):
    comment = read_markdown(comment_path)
    issue = get_issue(git_integration, payload)
    create_comment(issue, comment)

def create_pr_comment(git_integration, payload, comment_path):
    comment = read_markdown(comment_path)
    pr = get_pr(git_integration, payload)
    create_comment(pr, comment)
