import os
import openai
from github import Github, Auth

# Function that fetches all the changed files from the PR
def get_pr_files(pr):
    """Fetches changed files from the PR."""
    
    return [f for f in pr.get_files()]


# Function that generates the review for the PR
def generate_review(file_name, patch):
    """Sends the file to the LLM and gets suggestions based on the prompt."""
    
    # Initialize OpenAI API
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Define the prompt
    prompt = f"""
    You are a code reviewer. Review the following code diff and suggest improvements,
    bug fixes, or style enhancements. Be concise.

    File: {file_name}
    Diff:
    {patch}
    """

    # Get the response
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


# Function that puts it all together
def main():
    """
    Puts it all together.
    """

    # Retrieve the env vars
    token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_number = int(os.environ["PR_NUMBER"])

    # Get the files that were changed in the PR
    github = Github(auth=Auth.Token(token))
    repo = github.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    files = get_pr_files(pr)

    # Loop through the files
    for f in files:
        # Only review actual differences
        if f.patch: 
            # Generate the review and issue the comment
            review_comment = generate_review(f.filename, f.patch)
            pr.create_issue_comment(f"**Review for {f.filename}:**\n{review_comment}")


# Main guard
if __name__ == "__main__":
    main()