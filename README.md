# WillKleidung - Kleidungs Marketplace

## 🚀 Projekt Übersicht

Eine vollständige Django-basierte E-Commerce-Plattform für Kleidungsverkauf mit Features von Vinted und Willhaben.

### ✨ Features

- **Benutzerregistrierung & Authentifizierung** - Sichere Konten mit Profilen
- **Produktverwaltung** - Erstelle, bearbeite, lösche Kleidungsangebote
- **Erweiterte Suche & Filter** - Nach Kategorie, Preis, Größe, Zustand filtern
- **Favoriten System** - Speichere interessante Angebote
- **Nachrichten** - Direkter Kontakt zwischen Käufer und Verkäufer
- **Bewertungssystem** - Sterne-Bewertungen für Verkäufer
- **Profilseiten** - Öffentliche Profile mit Verkäufendaten
- **Admin-Panel** - Vollständiges Django Admin für Verwaltung
- **Responsive Design** - Bootstrap 5 Frontend für alle Geräte

---

## 📁 Projektstruktur

```
WillKleidung1/
├── WillKleidung1/              # Main Django Project
│   ├── settings.py             # Django Settings (Deutsch, Media, Templates)
│   ├── urls.py                 # Hauptrouten
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
│
├── Kleidung/                   # Main App
│   ├── models.py               # Datenbank-Modelle (Category, Listing, etc.)
│   ├── views.py                # Views (Home, Detail, Search, etc.)
│   ├── forms.py                # Django Forms (Listing, User, Search)
│   ├── urls.py                 # URL-Konfiguration
│   ├── admin.py                # Admin-Registrierung
│   └── migrations/             # Datenbankmigrationen
│
├── templates/                  # HTML-Templates
│   ├── base.html               # Base Template (Navigation, Footer)
│   ├── index.html              # Startseite
│   ├── auth/
│   │   ├── login.html          # Login-Seite
│   │   └── register.html       # Registrierung-Seite
│   ├── listings/
│   │   ├── detail.html         # Angebot-Detailseite
│   │   ├── create.html         # Angebot erstellen
│   │   ├── edit.html           # Angebot bearbeiten
│   │   ├── delete.html         # Angebot löschen
│   │   ├── my_listings.html    # Meine Angebote
│   │   └── search.html         # Suche & Filter
│   ├── messages/
│   │   ├── inbox.html          # Natrag-Posteingang
│   │   └── send.html           # Nachricht senden
│   ├── users/
│   │   ├── profile.html        # Benutzer-Profil
│   │   └── edit_profile.html   # Profil bearbeiten
│   ├── reviews/
│   │   └── add_review.html     # Bewertung abgeben
│   └── favorites.html          # Favoriten-Seite
│
├── static/                     # Statische Dateien
│   ├── css/                    # CSS-Dateien
│   ├── js/                     # JavaScript
│   └── img/                    # Bilder
│
├── media/                      # Benutzer-Uploads
│   └── listings/               # Produktbilder
│       profiles/               # Profilbilder
│
├── manage.py                   # Django Management
├── requirements.txt            # Python Dependencies
├── db.sqlite3                  # SQLite Datenbank (wird erstellt)
└── .gitignore                  # Git Ignore
```

---

## 🗄️ Datenbank-Modelle

### Category
- name, description, gender, icon

### Size
- size, category (FK)

### Listing
- seller (FK), title, description, category (FK), price, color, material, brand
- condition (Neu/Vintage/Sehr Gut/Gut), status (Aktiv/Verkauft/Reserviert)
- location, views, created_at, updated_at

### ListingImage
- listing (FK), image, is_primary, uploaded_at

### Favorite
- user (FK), listing (FK), created_at

### Message
- sender (FK), recipient (FK), listing (FK), subject, text
- created_at, is_read

### Review
- reviewer (FK), seller (FK), rating (1-5), comment, created_at

### UserProfile
- user (OneToOne), biography, profile_picture, location, phone, is_verified

---

## 🛠️ Installation & Verwendung

### 1. Virtuelle Umgebung aktivieren
Unter Windows (PowerShell):
```powershell
.\python\scripts\Activate.ps1
```

### 2. Requirements installieren
```bash
pip install -r requirements.txt
pip install Pillow  # Für Bildbearbeitung
```

### 3. Datenbank initialisieren
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Superuser erstellen (Admin)
```bash
python manage.py createsuperuser
```
Folge den Anweisungen zur Erstellung eines Admin-Kontos.

### 5. Beispieldaten laden (Optional)
```bash
python manage.py shell
# Dann in der Python-Shell:
from Kleidung.models import Category
Category.objects.create(name="Damenjacken", gender="M", description="Jacken für Damen")
Category.objects.create(name="Herrenhemd", gender="F", description="Hemden für Herren")
# ... mehr Kategorien
exit()
```

### 6. Entwicklungsserver starten
```bash
python manage.py runserver
```

Öffne http://127.0.0.1:8000 im Browser.

---

## 🔐 Admin Panel

Zugang: http://127.0.0.1:8000/admin/

Im Admin Panel kannst du:
- Kategorien und Größen verwalten
- Angebote moderieren
- Benutzer verwalten
- Nachrichten anschauen
- Bewertungen sehen
- Reviews lesen

---
## 🔧 Frontend (optional React/Vite)

Ein leichtes React-Projekt befindet sich im Ordner `frontend`. Es greift per Proxy auf die Django-API zu.

```bash
# im Projektverzeichnis
cd frontend
npm install
npm run dev   # startet Vite auf http://localhost:3000
```

Route-Beispiel: `http://localhost:3000/`

*Nur nötig, wenn du ein separates SPA bauen möchtest.*
## � API-Endpunkte

Der Server bietet eine JSON-API über Django REST Framework mit JWT-Authentifizierung.

- `GET /api/listings/` – Listings abfragen
- `POST /api/listings/` – neues Listing (JWT erforderlich)
- `GET /api/categories/`
- `GET /api/users/`
- `GET/POST /api/favorites/` – persönliche Favoriten (JWT)
- `GET/POST /api/messages/` – Nachrichten (JWT)
- `GET/POST /api/reviews/` – Bewertungen (JWT)

JWT-Token bekommen:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d '{"username":"user","password":"pass"}' -H "Content-Type: application/json"
```

Antwort enthält `access` und `refresh` Token. Refresh:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ -d '{"refresh":"<token>"}' -H "Content-Type: application/json"
```

Für lokale Frontends ist CORS für `http://localhost:3000` freigeschaltet.

---

## �📝 URL-Struktur

```
/                           # Startseite
/register/                  # Registrierung
/login/                     # Login
/logout/                    # Logout

/listing/<id>/              # Angebot-Detail
/listing/create/            # Neues Angebot
/listing/<id>/edit/         # Angebot bearbeiten
/listing/<id>/delete/       # Angebot löschen
/my-listings/               # Meine Angebote

/listing/<id>/favorite/     # Zu Favoriten (AJAX)
/favorites/                 # Meine Favoriten

/search/                    # Suche & Filter

/messages/                  # Posteingang
/message/<id>/send/         # Nachricht an Benutzer
/message/<id>/              # Nachricht anschauen

/profile/<username>/        # Benutzer-Profil
/profile/edit/              # Profil bearbeiten
/review/<user_id>/add/      # Bewertung abgeben

/admin/                     # Admin Panel
```

---

## 🎨 Frontend Features

- **Bootstrap 5** - Modernes, responsive Design
- **Font Awesome Icons** - 6.5.1
- **Bildgalerie** - Carousel für Produktbilder
- **Favoriten** - Client-seitige AJAX-Interaktion
- **Nachrichten-System** - Echtzeit-Chat (vereinfacht)
- **Filter & Suche** - Erweiterte Filteroptionen

---

## 🔧 Konfiguration

### settings.py wichtige Einstellungen:

```python
# Sprache & Zeitzone
LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Vienna'

# Media (Benutzer-Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Login/Logout URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
```

---

## 🚀 Produktions-Deployment

Für Production:

1. `DEBUG = False` in settings.py
2. Environment-Variablen für SECRET_KEY
3. ALLOWED_HOSTS konfigurieren
4. PostgreSQL statt SQLite verwenden
5. Collectstatic laufen:
   ```bash
   python manage.py collectstatic
   ```
6. CSRF_TRUSTED_ORIGINS einstellen
7. Gunicorn oder ähnlicher WSGI-Server

---

## 👥 Team-Features zur Erweiterung

- **Echtzeit-Benachrichtigungen** (Channels/Celery)
- **Sichere Zahlungen** (Stripe Integration)
- **Versandintegration** (DPD, GLS)
- **Rechteverifikation** (Photo ID)
- **Zwei-Faktor-Authentifizierung** (2FA)
- **Social Login** (Google, Facebook)
- **Empfehlungsengine** (Machine Learning)
- **APIs** (REST/GraphQL für Mobile Apps)

---

## 📧 Support

Bei Fragen weitere Django-Dokumentation:
- Django Docs: https://docs.djangoproject.com
- Bootstrap: https://getbootstrap.com
- Pillow: https://pillow.readthedocs.io

---

**Viel Spaß mit WillKleidung! 🎉**
