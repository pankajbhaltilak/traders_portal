import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traders_portal.settings")  # update to your settings module
django.setup()

from core.models import Company

def import_companies_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    count = 0
    for _, row in df.iterrows():
        # Defensive check: make sure required fields are not missing
        if pd.isna(row['company_name']) or pd.isna(row['symbol']) or pd.isna(row['scripcode']):
            continue

        company, created = Company.objects.get_or_create(
            scripcode=int(row['scripcode']),
            defaults={
                'company_name': row['company_name'],
                'symbol': row['symbol'],
            }
        )
        if created:
            count += 1

    print(f"✅ Imported {count} new companies.")

if __name__ == "__main__":
    csv_file_path = 'master.csv'  # your CSV filename
    import_companies_from_csv(csv_file_path)
