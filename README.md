Usage
-----

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your API key (PowerShell):

```powershell
$env:OPENROUTER_API_KEY = "sk-..."
# or to persist: setx OPENROUTER_API_KEY "sk-..."
```

3. Run the script with an optional message:

```bash
python API.py "Hello from me"
```

If no message is provided, the script will ask "What is the meaning of life?" by default.

Web UI
------

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set `OPENROUTER_API_KEY` (PowerShell):

```powershell
$env:OPENROUTER_API_KEY = "sk-..."
```

3. Run the web server:

```bash
python index.py
```

Open http://localhost:5000 in your browser.
