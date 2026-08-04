import pandas as pd

from django.core.management.base import BaseCommand
from accounts.models import State, District, SubDistrict


class Command(BaseCommand):
    help = "Import LGD Data"

    def handle(self, *args, **kwargs):

        # Read Excel File
        df = pd.read_excel("All_Sub_Districts.xlsx")

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():

            # Skip empty rows
            if pd.isna(row["State"]):
                continue

            if pd.isna(row["District"]):
                continue

            if pd.isna(row["Sub-district"]):
                continue

            state_name = row["State"].strip()
            district_name = row["District"].strip()
            subdistrict_name = row["Sub-district"].strip()

            state, _ = State.objects.get_or_create(
                name=state_name
            )

            district, _ = District.objects.get_or_create(
                state=state,
                name=district_name
            )

            SubDistrict.objects.get_or_create(
                district=district,
                name=subdistrict_name
            )

        self.stdout.write(
            self.style.SUCCESS("LGD Data Imported Successfully")
        )