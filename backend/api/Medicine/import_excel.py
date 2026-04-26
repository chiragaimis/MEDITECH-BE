import os
import sys
import django
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

# PROJECT ROOT (where manage.py lives)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.insert(0, BASE_DIR)

ENV = os.getenv("ENV", "local")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"backend.settings.{ENV}"
)

django.setup()

from api.Medicine.model import Medicine



# --------------------------------------------------
# Import AFTER django.setup()
# --------------------------------------------------
from api.Medicine.model import Medicine

# --------------------------------------------------
# Excel file path
# --------------------------------------------------
EXCEL_FILE_PATH = r"D:\Medicine.xlsx"

# --------------------------------------------------
# Import logic
# --------------------------------------------------
def import_medicines():
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return

    created = 0
    skipped = 0

    for index, row in df.iterrows():
        medicine_name = str(row.get("medicine_name", "")).strip()
        full_description = str(row.get("full_description", "")).strip()
        dose = str(row.get("dose", "")).strip()

        if not medicine_name or not full_description:
            print(f"❌ Row {index + 2}: medicine_name or description missing")
            skipped += 1
            continue

        if Medicine.objects.filter(medicine_name__iexact=medicine_name).exists():
            print(f"⚠️ Skipped duplicate: {medicine_name}")
            skipped += 1
            continue

        Medicine.objects.create(
            medicine_name=medicine_name,
            full_description=full_description,
            dose=None if dose.lower() == "nan" or dose == "" else dose
        )

        print(f"✅ Inserted: {medicine_name}")
        created += 1

    print("\n🎉 Import Completed")
    print(f"✅ Created: {created}")
    print(f"⚠️ Skipped: {skipped}")


if __name__ == "__main__":
    import_medicines()
