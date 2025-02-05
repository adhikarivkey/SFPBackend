import pandas as pd
from django.core.management.base import BaseCommand
from api.models import GasStation


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            csv_file = "fuel-prices-for-be-assessment.csv"
            df = pd.read_csv(csv_file)
            filter_df = df.loc[df.groupby(['OPIS Truckstop ID', 'City', 'State']
                                          )['Retail Price'].idxmin()]

            for _, row in filter_df.iterrows():
                GasStation.objects.update_or_create(truckstop_id=row['OPIS Truckstop ID'],
                                                    defaults={
                                                        'name': row['Truckstop Name'],
                                                        'address': row['Address'],
                                                        'city': row['City'],
                                                        'state': row['State'],
                                                        'price': row['Retail Price'],
                                                        'rack_id': row['Rack ID']
                                                    })
            self.stdout.write(self.style.SUCCESS(f'Imported {len(filter_df)} Gas stations'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_file}"))
            return
        except:
            self.stdout.write(self.style.ERROR(f"Something Went Wrong"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"{GasStation.objects.count()} Gas stations in database.")
        )
        self.stdout.write(self.style.SUCCESS("Station import completed"))
