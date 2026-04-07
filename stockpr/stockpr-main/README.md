 .venv311\Scripts\Activate.ps1


# Stock Prediction Project

This workspace contains a Flask-based front-end and some ML components (TensorFlow/Keras).

Quick start — Run the Flask site only

1. Open PowerShell and change directory:

```powershell
cd "c:\Users\user\Desktop\final_stockprdiction\stockpr-main - Copy\stockpr-main"
```

2. Create a virtual environment and install minimal deps:

```powershell
python -m venv .venv
.venv\Scripts\pip.exe install --upgrade pip
.venv\Scripts\pip.exe install Flask Flask_SQLAlchemy Werkzeug python-dotenv
```

3. (Optional) copy `.env.example` to `.env` and set `SECRET_KEY`:

```powershell
copy .env.example .env
# edit .env with a secure SECRET_KEY
```

4. Run the app:

```powershell
.venv\Scripts\python.exe app.py
```

Visit: http://127.0.0.1:5000

Full ML stack (TensorFlow) — recommended approach

TensorFlow requires a specific Python version. The system currently has Python 3.14 which is not compatible with many TensorFlow builds.

1. Install Python 3.10 or 3.11 from https://www.python.org/downloads/ if you don't have it.
2. Create a new venv using that interpreter (replace `py -3.10` with the correct launcher if needed):

```powershell
py -3.10 -m venv .venv_py310
.venv_py310\Scripts\python.exe -m pip install --upgrade pip
.venv_py310\Scripts\pip.exe install -r requirements.txt
```

3. If `pip install -r requirements.txt` fails on `tensorflow`, install a specific version that matches your Python, for example:

```powershell
.venv_py310\Scripts\pip.exe install tensorflow==2.11.0
```

Notes
- Project contains both Flask and some Django-related files (`manage.py`). The Django project `StockPulse` isn't present in this repository — I focused on getting the Flask app running.
- I updated `app.py` to read `SECRET_KEY` and `DATABASE_URL` from environment variables and fixed a template path.

Next steps I can do for you
- Finish wiring templates/links and add user registration validation.
- Create a Dockerfile for reproducible environments.
- Attempt the full `pip install -r requirements.txt` inside a Python 3.10 venv and resolve any package-specific issues.

Which next step should I take? (I can create the Python 3.10 venv and attempt a full install if you want.)
