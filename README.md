# Medical Research Database - In Vitro/In Vivo Documentation System

System zarządzania badaniami medycznymi z obsługą kompleksowych modeli danych dla badań in vitro (linie komórkowe) i in vivo (modele zwierzęce).

## 🎯 Funkcjonalności

- ✅ **Kompleksowe modele danych** - Linie komórkowe, modele zwierzęce, protokoły, eksperymenty
- ✅ **Relacje N-M** - Wsparcie dla skomplikowanych relacji między encjami
- ✅ **RESTful API** - Pełne API z autentykacją, filtrowaniem i wyszukiwaniem
- ✅ **Raporty** - Generowanie raportów wyników i ekspresji genów
- ✅ **Django Admin** - Intuicyjny interfejs zarządzania danymi
- ✅ **Dokumentacja** - System notatek i załączników do eksperymentów
- ✅ **Ekspresja genów** - Obsługa qPCR, RNA-Seq, Microarray, In Situ
- ✅ **Filtrowanie zaawansowane** - Wyszukiwanie, sortowanie, filtry

## 🛠️ Technologia

- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Baza danych**: SQLite (dev) / PostgreSQL (production)
- **Python**: 3.10+

## 🚀 Szybki start

### 1. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 2. Migruj bazę danych
```bash
python manage.py migrate
```

### 3. Załaduj przykładowe dane
```bash
python populate_data.py
```

### 4. Uruchom serwer
```bash
python manage.py runserver
```

**Dostęp:**
- Admin: http://localhost:8000/admin/ (admin/admin123)
- API: http://localhost:8000/api/

## 📚 Dokumentacja

Pełna dokumentacja dostępna w [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 📖 API Endpoints

### Modele
- `/api/cell-lines/` - Linie komórkowe
- `/api/animal-models/` - Modele zwierzęce
- `/api/protocols/` - Protokoły badań
- `/api/experiments/` - Eksperymenty
- `/api/samples/` - Próbki in vitro
- `/api/animals/` - Zwierzęta in vivo
- `/api/results/` - Wyniki
- `/api/gene-expressions/` - Ekspresja genów
- `/api/documentation/` - Dokumentacja

### Autentykacja
```bash
POST /api/auth/token/ - Uzyskaj token (username/password)
```

## 🔐 Dostęp do API

```bash
# Uzyskaj token
curl -X POST http://localhost:8000/api/auth/token/ \
  -d '{"username": "admin", "password": "admin123"}'

# Użyj w requestach
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/experiments/
```

## 📁 Struktura
- `research/models.py` - Modele bazy danych
- `research/serializers.py` - REST serializers
- `research/views.py` - API ViewSets
- `research/admin.py` - Django Admin
- `populate_data.py` - Generowanie testowych danych

## 📄 Licencja
MIT - dostępne do celów edukacyjnych i badawczych
