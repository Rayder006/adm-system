import os
import subprocess

def load_fixtures():
    fixtures_dir = "./main/fixtures/"
    fixtures = [f for f in os.listdir(fixtures_dir) if f.endswith(".json")]

    for fixture in fixtures:
        fixture_path = os.path.join(fixtures_dir, fixture)
        cmd = f"python manage.py loaddata {fixture_path}"
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    load_fixtures()
