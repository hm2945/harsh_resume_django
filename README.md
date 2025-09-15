# Django Resume — HTML generated via template tags

This project renders my resume using Django's template system **without** hard-coding any HTML in the views.

---

## Run it locally (Python 3.10+)

### 1) Clone the repo
```bash
git clone https://github.com/hm2945/harsh_resume_django.git
cd harsh_resume_django
```

### 2) Create and activate a virtual environment

Powershell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install requirements
```bash
pip install -r requirements.txt
```
### 4) (Optionally) Apply migrations
```bash
python manage.py migrate
```

### 5) Run the server
```bash
python manage.py runserver
```

Open Resume @ : http://127.0.0.1:8000/