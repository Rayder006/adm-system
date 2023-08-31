import os
import django

# Configurar o ambiente do Django manualmente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.core.management import call_command

# def load_fixtures():
#     fixtures_dir = "./main/fixtures/"
#     fixtures = [f for f in os.listdir(fixtures_dir) if f.endswith(".json")]

#     for fixture in fixtures:
#         fixture_path = os.path.join(fixtures_dir, fixture)
#         call_command("loaddata", fixture_path)
#         print(fixture_path)

if __name__ == "__main__":
    # load_fixtures()
    call_command("loaddata", "./main/fixtures/1-account_type.json")
    call_command("loaddata", "./main/fixtures/2-account.json")
    call_command("loaddata", "./main/fixtures/3-gender.json")
    call_command("loaddata", "./main/fixtures/4-sale_origin.json")
    call_command("loaddata", "./main/fixtures/5-sale_status.json")
    call_command("loaddata", "./main/fixtures/6-sale_type.json")
    call_command("loaddata", "./main/fixtures/7-payment_type.json")
    call_command("loaddata", "./main/fixtures/8-sale_service.json")
