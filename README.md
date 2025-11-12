# Django Portfolio - Geospatial User Profile System

A Django-based user profile management system with geospatial capabilities, featuring interactive maps, role-based access control, and comprehensive activity tracking.

## 📋 Features

### Core Requirements ✅
- **Extended User Profiles**: Home address, phone number, and geographic location (PostGIS Point geometry)
- **Profile Management**: View and edit pages (users can only access their own profile)
- **Interactive Map**: Full-screen Leaflet map displaying all registered users' locations
- **Marker Popups**: Click user markers to view profile information
- **Authentication**: Login via Django admin page
- **Access Control**: Only superusers can access Django admin for all models
- **Role-Based Data**: Normal users see limited info, superusers see full details

### Bonus Features ✅
- **Test Suite**: Comprehensive unit tests covering models, views, and access control
- **CI/CD Integration**: GitHub Actions workflow with automated testing on PRs
- **Login Activity Tracking**: Logs all user login/logout events with IP and user agent
- **Custom Admin Site**: Superuser-only admin interface with enhanced security

## 🛠️ Technology Stack

- **Framework**: Django 5.1.2 with GeoDjango
- **Database**: PostgreSQL 16 + PostGIS 3.4 (production), SQLite (local fallback)
- **Mapping**: Leaflet.js with django-leaflet 0.31.0
- **Frontend**: Pico CSS 2.0 for clean, minimal styling
- **Server**: Gunicorn 22.0.0 WSGI server
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions
- **Python**: 3.12

## 🚀 Getting Started

### Prerequisites

Choose one of the following options:

**Option 1: Docker (Recommended)**
- Docker Desktop installed
- Full PostGIS/GIS functionality

**Option 2: Local Development**
- Python 3.12 installed
- Limited GIS functionality (SQLite fallback)

### Installation & Setup

#### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd django-portfolio
```

2. **Start the application**
```bash
docker compose up --build
```

3. **Create database migrations** (in another terminal)
```bash
docker compose exec web python manage.py makemigrations profiles
docker compose exec web python manage.py migrate
```

4. **Create a superuser account**
```bash
docker compose exec web python manage.py createsuperuser
```

5. **Access the application**
- App: http://localhost:8000
- Admin: http://localhost:8000/admin/

#### Option 2: Local Development (Windows)

1. **Clone the repository**
```bash
git clone <repository-url>
cd django-portfolio
```

2. **Create and activate virtual environment**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**
```powershell
pip install -r requirements-local.txt
```

4. **Set environment variable for SQLite**
```powershell
$env:USE_SQLITE="1"
```

5. **Run migrations**
```powershell
python manage.py makemigrations profiles
python manage.py migrate
```

6. **Create superuser**
```powershell
python manage.py createsuperuser
```

7. **Start development server**
```powershell
python manage.py runserver
```

8. **Access the application**
- App: http://localhost:8000
- Admin: http://localhost:8000/admin/

**Note**: Local mode uses SQLite without PostGIS, so geographic features are limited.

## 🧪 Running Tests

### With Docker
```bash
docker compose run --rm web bash -lc "python manage.py test -v 2"
```

### Locally
```bash
python manage.py test -v 2
```

### Test Coverage

The test suite includes:
- Profile auto-creation on user creation
- Authentication requirements for protected views
- Profile viewing and editing functionality
- Point geometry creation from lat/lng coordinates
- Role-based data filtering (normal users vs superusers)
- GeoJSON API endpoint access control

## 📖 Usage Guide

### For Regular Users

1. **Login**: Navigate to http://localhost:8000/admin/login/
2. **View Profile**: Click "My Profile" in navigation
3. **Edit Profile**: Click "Edit profile" button
   - Enter home address and phone number
   - Click on the map to set your location, or enter coordinates manually
   - Save changes
4. **View Map**: Click "Map" to see all users' locations
   - Click markers to view user information
   - Normal users see only usernames for other users

### For Superusers

- **Admin Access**: Full access to Django admin at /admin/
- **View All Data**: See complete profile information (address, phone) for all users on the map
- **Manage Models**: Access Profile and LoginActivity models in admin
- **Monitor Activity**: View login/logout events with IP addresses and timestamps

## 🏗️ Project Structure

```
portfolio/              # Django project configuration
├── settings.py        # Configuration and installed apps
├── urls.py            # Root URL routing
├── admin.py           # Custom superuser-only admin site
├── wsgi.py            # WSGI entry point
└── asgi.py            # ASGI entry point

profiles/              # Main application
├── models.py          # Profile and LoginActivity models
├── views.py           # View classes and functions
├── forms.py           # ProfileForm with Leaflet widget
├── urls.py            # App URL patterns
├── admin.py           # Admin model registration
├── signals.py         # Signal handlers for auto-creation and logging
├── tests.py           # Test suite
└── apps.py            # App configuration

templates/             # Template files
├── base.html          # Base template with navigation
└── profiles/          # Profile-specific templates
    ├── home.html
    ├── my_profile.html
    ├── edit_my_profile.html
    └── users_map.html
```

## 🔒 Security & Access Control

- **Profile Access**: Users can only view and edit their own profile
- **Admin Access**: Only superusers can access /admin/
- **Data Filtering**: Role-based filtering in GeoJSON API
  - Normal users: See only usernames
  - Superusers: See full profile details
- **CSRF Protection**: All forms include CSRF tokens
- **Password Security**: Django's built-in password hashing and validation

## 🌍 API Endpoints

### GeoJSON API
**Endpoint**: `/api/users-geojson/`  
**Method**: GET  
**Authentication**: Required  
**Response**: GeoJSON FeatureCollection with user locations

**Example Response**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      },
      "properties": {
        "username": "john",
        "home_address": "123 Main St",  // Only for superusers
        "phone_number": "555-1234",     // Only for superusers
        "profile_url": "/me/"            // Only for own profile
      }
    }
  ]
}
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Auto-generated |
| `DJANGO_DEBUG` | Debug mode | `1` (enabled) |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `USE_SQLITE` | Use SQLite instead of PostgreSQL | Not set |
| `POSTGRES_DB` | PostgreSQL database name | `portfolio` |
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` |
| `POSTGRES_HOST` | PostgreSQL host | `db` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |

## 🤝 Contributing

This project follows best practices for code quality:

1. **Meaningful Commits**: Each commit represents a logical unit of work
2. **Clear Messages**: Commit messages explain the intent of changes
3. **Documentation**: All functions and classes have docstrings
4. **Code Style**: Clean, readable code with descriptive variable names
5. **Testing**: Comprehensive test coverage for all features

## 📝 Development Notes

- Code uses tabs for indentation for consistency
- All models, views, forms, and signals include comprehensive docstrings
- Variable names are descriptive and indicate their purpose
- PostGIS `PointField` uses `geography=True` for accurate Earth-surface calculations
- Point geometry uses (longitude, latitude) order (X, Y coordinates)
- Signals handle automatic profile creation and activity logging
- Custom admin site enforces superuser-only access

## 📄 License

This project was created as an assignment demonstration.

## 🙏 Acknowledgments

- Django and GeoDjango teams for the excellent framework
- PostGIS for powerful geospatial database capabilities
- Leaflet.js for interactive mapping
- OpenStreetMap for map tiles


