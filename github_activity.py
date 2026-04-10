import sys
import urllib.request
import json

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Usuário não encontrado.")
        else:
            print("Erro ao acessar a API.")
        return None
    except Exception as e:
        print("Erro inesperado:", e)
        return None

def format_event(event):
    event_type = event.get("type")
    repo_name = event.get("repo", {}).get("name", "repositório desconhecido")

    if event_type == "PushEvent":
        commits = len(event.get("payload", {}).get("commits", []))
        
        if commits > 0:
            return f"Pushed {commits} commits to {repo_name}"
        else:
            return f"Pushed commits to {repo_name}"

    elif event_type == "IssuesEvent":
        action = event.get("payload", {}).get("action", "updated")
        return f"{action.capitalize()} an issue in {repo_name}"

    elif event_type == "WatchEvent":
        return f"Starred {repo_name}"

    elif event_type == "ForkEvent":
        return f"Forked {repo_name}"

    elif event_type == "CreateEvent":
        ref_type = event.get("payload", {}).get("ref_type", "something")
        return f"Created {ref_type} in {repo_name}"

    return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python github_activity.py <username>")
        return

    username = sys.argv[1]

    events = fetch_github_activity(username)

    if not events:
        return

    for event in events[:10]:
        formatted = format_event(event)
        if formatted:
            print(f"- {formatted}")

if __name__ == "__main__":
    main()
