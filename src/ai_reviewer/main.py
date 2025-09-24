import os
import openai
from github import Github

def get_pr_files(pr):
    """Fetches changed files from the PR."""
    
    return [f for f in pr.get_files()]

def generate_review(file_name, patch):
    """Sends the file to the LLM and gets suggestions based on the prompt."""
    
    # Initialize 
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    prompt = f"""
    You are a code reviewer. Review the following code diff and suggest improvements,
    bug fixes, or style enhancements. Be concise.

    File: {file_name}
    Diff:
    {patch}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
    )
    return response.choices[0].message.content

def main():
    """
    Puts it all together.
    """
    token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_number = int(os.environ["PR_NUMBER"])

    github = Github(token)
    repo = github.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    files = get_pr_files(pr)

    for f in files:
        if f.patch: # Only review actual differences
            review_comment = generate_review(f.filename, f.patch)
            pr.create_issue_comment(f"**Review for {f.filename}:**\n{review_comment}")

# Main guard
if __name__ == "__main__":
    main()
