#  START HERE - Medical Research Database

> **NOTE:** API endpoints have been removed from the backend on branch `remove-api` — documentation may reference legacy API.

##  Szybki Start (5 minut)

### 1️ Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 2️ Migruj bazę danych
```bash
python manage.py migrate
```

### 3️ Załaduj przykładowe dane
```bash
python populate_data.py
```

### 4️ Uruchom serwer
```bash
python manage.py runserver
```

### 5️ Otwórz w przeglądarce
- **Admin**: http://localhost:8000/admin/
  - Login: `admin` / `admin123`

> **Uwaga:** API została usunięta z backendu na branchu `remove-api`. Dokumentacja i przykłady API mogą być nieaktualne.

---

##  Dokumentacja

| Plik | Zawartość |
|------|-----------|
| **README.md** | Szybki przegląd funkcji |
| **API_DOCUMENTATION.md** | Pełna dokumentacja API z przykładami |
| **TECHNICAL_DOCUMENTATION.md** | Dokumentacja architekturalneaj |
| **PROJECT_SUMMARY.md** | Statystyki i podsumowanie |
| **GITHUB_SETUP.md** | Jak opublikować na GitHub |

 **Zacznij od: README.md**

---

##  Co to jest?

System do zarządzania badaniami medycznymi z:
-  **9 modeli danych** (linie komórkowe, modele zwierzęce, eksperymenty, itp.)
-  **RESTful API** (90+ endpoints)
-  **Django Admin** (interfejs webowy)
-  **Raporty** (podsumowania, statystyki)
-  **Autoryzacja** (token-based)

---

##  Autentykacja API

### Uzyskaj token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Użyj w requestach
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/experiments/
```

---

##  Struktura projektu

```
medical-research-db/
├── research/              # Główna aplikacja
│   ├── models.py         # 9 modeli danych
│   ├── views.py          # API endpoints
│   ├── serializers.py    # Serializery
│   └── admin.py          # Django Admin
├── hello_world/          # Konfiguracja Django
├── populate_data.py      # Generator danych
└── manage.py             # Django CLI
```

---

## 🧪 Testy API

### Lista eksperymentów
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/experiments/
```

### Filtrowanie
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/experiments/?status=ongoing"
```

### Wyszukiwanie
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/cell-lines/?search=HeLa"
```

### Raport eksperymentu
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/experiments/1/summary/
```

---

## 🎓 Modele danych

1. **CellLine** - Linie komórkowe (in vitro)
2. **AnimalModel** - Modele zwierzęce (in vivo)
3. **ResearchProtocol** - Protokoły badań
4. **Experiment** - Główne eksperymenty
5. **ExperimentSample** - Próbki (N-M)
6. **ExperimentAnimal** - Zwierzęta w eksperymentach (N-M)
7. **Result** - Wyniki pomiarów
8. **GeneExpression** - Ekspresja genów
9. **Documentation** - Notatki i dokumenty

---

## 🚀 Następne kroki

### Dla lokalnej pracy
1. Czytaj API_DOCUMENTATION.md
2. Eksploruj API w http://localhost:8000/api/
3. Dodaj nowe dane w Django Admin

### Dla GitHub
1. Czytaj GITHUB_SETUP.md
2. Stwórz repo na GitHub
3. Wyślij kod: `git push -u origin main`

### Dla produkcji
1. Czytaj TECHNICAL_DOCUMENTATION.md
2. Zmień na PostgreSQL
3. Deploy na Heroku/DigitalOcean/AWS

---

## ⚙️ Polecane komendy

```bash
# Django Admin
python manage.py createsuperuser

# Migracje
python manage.py makemigrations
python manage.py migrate

# Shell
python manage.py shell

# Testy
python manage.py test research

# Statyczne pliki
python manage.py collectstatic
```

---

## 🆘 Potrzebujesz pomocy?

- **API Reference**: API_DOCUMENTATION.md
- **Architecture**: TECHNICAL_DOCUMENTATION.md
- **Overview**: PROJECT_SUMMARY.md
- **GitHub**: GITHUB_SETUP.md

---

## 💡 Szybkie tipy

- Admin panel jest bardzo przydatny do zarządzania danymi
- API supports filtering, searching, and sorting
- Sample data już załadowana - możesz testować od razu
- Token auth wymagany dla API (nie dla Admin)

---

## ✨ Wbudowane dane

- 4 linie komórkowe (HeLa, HEK293, MCF-7, CHO)
- 3 modele zwierzęce (myszy, szczury)
- 3 komplentne eksperymenty z danymi
- 12 pomiarów ekspresji genów

---

**Powodzenia w pracy! 🚀**

*Pytania? Sprawdź dokumentację.*

