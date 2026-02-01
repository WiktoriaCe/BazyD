# 🚀 START HERE - Medical Research Database

## Witaj! 👋

Właśnie pobrałeś/pobrałaś kompleksowy system zarządzania badaniami medycznymi w Django.

## ⚡ Szybki Start (5 minut)

### 1️⃣ Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 2️⃣ Migruj bazę danych
```bash
python manage.py migrate
```

### 3️⃣ Załaduj przykładowe dane
```bash
python populate_data.py
```

### 4️⃣ Uruchom serwer
```bash
python manage.py runserver
```

### 5️⃣ Otwórz w przeglądarce
- **Admin**: http://localhost:8000/admin/
  - Login: `admin` / `admin123`

---

## 📚 Dokumentacja

| Plik | Zawartość |
|------|-----------|
| **README.md** | Szybki przegląd funkcji |
| **TECHNICAL_DOCUMENTATION.md** | Dokumentacja architekturalna |
| **PROJECT_SUMMARY.md** | Statystyki i podsumowanie |
| **GITHUB_SETUP.md** | Jak opublikować na GitHub |

👉 **Zacznij od: README.md**

---

## 🎯 Co to jest?

System do zarządzania badaniami medycznymi z:
- ✅ **9 modeli danych** (linie komórkowe, modele zwierzęce, eksperymenty, itp.)
- ✅ **Django Admin** (interfejs webowy)
- ✅ **Raporty** (podsumowania, statystyki)
- ✅ **Autoryzacja** (token-based)

---


---

## 📊 Struktura projektu

```
medical-research-db/
├── research/              # Główna aplikacja
│   ├── models.py         # 9 modeli danych
│   ├── views.py          # Site views and admin helpers
│   └── admin.py          # Django Admin
│   └── admin.py          # Django Admin
├── hello_world/          # Konfiguracja Django
├── populate_data.py      # Generator danych
└── manage.py             # Django CLI
```

---

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
1. Dodaj nowe dane w Django Admin
2. Skontaktuj się, jeśli chcesz wprowadzić nowe integracje

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

- **Architecture**: TECHNICAL_DOCUMENTATION.md
- **Overview**: PROJECT_SUMMARY.md
- **GitHub**: GITHUB_SETUP.md

---

## 💡 Szybkie tipy

- Admin panel jest bardzo przydatny do zarządzania danymi
- Sample data już załadowana - możesz testować od razu

---

## ✨ Wbudowane dane

- 4 linie komórkowe (HeLa, HEK293, MCF-7, CHO)
- 3 modele zwierzęce (myszy, szczury)
- 3 komplentne eksperymenty z danymi
- 12 pomiarów ekspresji genów

---

**Powodzenia w pracy! 🚀**

*Pytania? Sprawdź dokumentację.*

