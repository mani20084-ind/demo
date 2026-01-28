import os
from github import Github

def mock_ai_planner(requirement_text):
    """
    SIMULATED AI with a safety check for empty descriptions.
    """
    # Safety Check: If body is empty, use a placeholder string
    text_to_print = requirement_text if requirement_text else "No description provided."
    
    print(f"🤖 AI is analyzing requirement: {text_to_print[:50]}...")
    
    return [
        {"title": "Task 1: Infrastructure Setup", "body": "Setup the environment and initial repo structure."},
        {"title": "Task 2: Core Feature Implementation", "body": "Develop the primary logic defined in the requirements."},
        {"title": "Task 3: Automated Testing & QA", "body": "Write unit tests and verify the deployment pipeline."}
    ]

def main():
    # 1. Setup Connection (GitHub provides these automatically in the Action)
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    issue_number = int(os.getenv("ISSUE_NUMBER"))

    g = Github(token)
    repo = g.get_repo(repo_name)
    mother_issue = repo.get_issue(number=issue_number)

    # 2. 'The Brain' processes the requirement
    tasks = mock_ai_planner(mother_issue.body)

    # 3. 'The Hands' create the new issues
    for task in tasks:
        new_issue = repo.create_issue(
            title=task["title"],
            body=f"{task['body']}\n\n---\n*Linked to Mother Requirement: #{issue_number}*",
            labels=["ai-generated-task"]
        )
        print(f"✅ Created issue: {new_issue.title} (#{new_issue.number})")

    # 4. Final confirmation comment
    mother_issue.create_comment("🎉 POC Success: The AI Orchestrator has generated 3 tasks based on your requirements.")

if __name__ == "__main__":
    main()
