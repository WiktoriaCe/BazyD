# GitHub Setup Guide

##  Publikacja projektu na GitHub

### Krok 1: Stwórz nowe repozytorium na GitHub

1. Wejdź na https://github.com/new
2. Nazwa: `medical-research-db`
3. Opis: `Django system for in vitro/in vivo research documentation with REST API`
4. Ustaw typ: Public (lub Private)
5. **NIE** inicjalizuj z README (już mamy)
6. Kliknij "Create repository"

### Krok 2: Połącz lokalne repo z GitHub

```bash
cd /workspaces/codespaces-django

# Dodaj remote
git remote add origin https://github.com/YOUR_USERNAME/medical-research-db.git

# Zmień gałąź na main (jeśli trzeba)
git branch -M main

# Push do GitHub
git push -u origin main
```

### Krok 3: Dodaj GitHub Actions (opcjonalnie)

Stwórz plik `.github/workflows/django.yml`:

```yaml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run migrations
      run: python manage.py migrate
    
    - name: Run tests
      run: python manage.py test research
```

## Checklist przed publikacją

- [ ] Zmień `SECRET_KEY` w `.env`
- [ ] Ustawić `DEBUG=False` dla produkcji
- [ ] Sprawdzić `ALLOWED_HOSTS` w settings.py
- [ ] Dodać `.env` do `.gitignore` (już jest)
- [ ] Usunąć `db.sqlite3` jeśli chcesz czystą bazę (Git go ignoruje)
- [ ] Sprawdzić migracje są committed
- [ ] Uruchomić testy: `python manage.py test research`

##  Konfiguracja dla Produkcji

### Plik `.env` (NIE commituj!)

```
SECRET_KEY=your-very-long-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/medical_research_db
```

##  Deployment Opcje

### 1. Heroku

```bash
# Zainstaluj Heroku CLI
# Login
heroku login

# Stwórz app
heroku create medical-research-db

# Ustaw zmienne
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key"

# Deploy
git push heroku main

# Migruj bazę
heroku run python manage.py migrate

# Stwórz superusera
heroku run python manage.py createsuperuser
```

### 2. PythonAnywhere

1. Zaloguj się na pythonanywhere.com
2. Załaduj kod z GitHub
3. Ustaw virtualenv
4. Skonfiguruj WSGI
5. Załaduj statyczne pliki: `collectstatic`

### 3. DigitalOcean / AWS / Azure

Użyj Gunicorn + Nginx + Postgres

##  README.md dla GitHub

Projekt zawiera kompletny README.md z:
- Quick start instrukcjami
- API dokumentacją
- Przykładami użycia
- Instrukcjami deployment

##  Sugerowane tagi/labels na GitHub

- `django` - Frameworka
- `rest-api` - API
- `medical-research` - Domena
- `database` - Typ projektu
- `n-m-relationships` - Funkcjonalność
- `python` - Język

##  Sugerowane tematy (Topics)

- django
- rest-api
- medical-research
- python
- database

##  CI/CD Pipeline (GitHub Actions)

Projekt jest gotowy dla automatycznych testów i deploymentu.

##  Support Links do Include

- Documentation: `/API_DOCUMENTATION.md`
- Technical: `/TECHNICAL_DOCUMENTATION.md`
- Project Summary: `/PROJECT_SUMMARY.md`

##  Commit History

Projekt ma czystą historię commitów:

1. **Initial commit**: Podstawowe setup
2. **Medical research database**: Główne modele, API, admin
3. **Technical documentation**: Dokumentacja architekturalneaj
4. **Project summary**: Podsumowanie i statystyki

##  Instrukcje dla Użytkowników

Po sklonowaniu repozytorium z GitHub:

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/medical-research-db.git
cd medical-research-db

# Setup
pip install -r requirements.txt
python manage.py migrate

# Załaduj dane (opcjonalnie)
python populate_data.py

# Run
python manage.py runserver

# Admin
# http://localhost:8000/admin/
# admin / admin123
```

##  Contributing Guide (opcjonalnie)

Możesz dodać `CONTRIBUTING.md` z instrukcjami dla contributors.

##  Licencja

Projekt zawiera domyślnie MIT License. Jeśli chcesz zmienić, stwórz plik `LICENSE`:

```
MIT License

Copyright (c) 2025 Medical Research Team

Permission is hereby granted, free of charge...
```



