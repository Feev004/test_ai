import os
import sys
import json
import requests


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: Set OPENROUTER_API_KEY environment variable first.", file=sys.stderr)
        sys.exit(1)

    # allow passing the user message via command-line args
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = "What is the meaning of life?"

    payload = {
        "model": "openrouter/owl-alpha",
        "messages": [{"role": "user", "content": user_message}],
    }

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
    except requests.RequestException as e:
        print("Request error:", e, file=sys.stderr)
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"API returned status {resp.status_code}", file=sys.stderr)
        try:
            print(resp.text, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)

    # print formatted JSON response
    try:
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except ValueError:
        print(resp.text)


if __name__ == "__main__":
    main()