import os
import sys

from django.conf import settings
from django.core.management import call_command

# Configuración básica de Django. Ajusta según sea necesario.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "oauth2_provider",
    "rest_framework",
    "auditlog",
    "django_json_widget",
    "import_export",
]

LOCAL_APPS = [
    "omni_pro_base",
    "omni_pro_oms",
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=INSTALLED_APPS,
    SECRET_KEY="django-insecure-_xm%ar7&b@9n84@bkgiy@m#cl_lhqdgpg*p(+l#ie%8dzw#51+",
    MIDDLEWARE=(
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
)

if __name__ == "__main__":
    # Asegúrate de que Django esté configurado para tu proyecto.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omni_pro_oms.mig_settings")
    try:
        # Inicializa las configuraciones de Django
        import django

        django.setup()

        # Genera las migraciones para tu aplicación
        call_command("makemigrations", "omni_pro_oms")

    except Exception as e:
        print(f"Error al generar migraciones: {e}")
        sys.exit(1)
