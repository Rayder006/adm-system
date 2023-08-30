import os
import django

# Configurar o ambiente do Django manualmente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.core.management import call_command

def load_fixtures():
    fixtures_dir = "./main/fixtures/"
    fixtures = [f for f in os.listdir(fixtures_dir) if f.endswith(".json")]

    for fixture in fixtures:
        fixture_path = os.path.join(fixtures_dir, fixture)
        call_command("loaddata", fixture_path)

if __name__ == "__main__":
    load_fixtures()
