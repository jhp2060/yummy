import datetime
import os

from django.core.management import BaseCommand, CommandError

from api.serializers import SikdanSerializer, DishUpdateSerializer
from api.models import *
import xlrd
import json

class Command(BaseCommand):
    help = 'update sikdan for every day'

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            nargs=1,
                            type=str,
                            help='name of excel file(.xlsx)')

    def handle(self, *args, **options):
        filename = options['filename'][0]
        try:
            self.sikdan_update(filename)
        except:
            raise CommandError("Failed updated sikdan")

    def sikdan_update(self, filename):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(BASE_DIR, 'excel_file.json'), 'rb') as f:
            excel = json.load(f)

        excel_file_base_path = excel['EXCEL_FILE_BASE_PATH']
        excel_file_path = excel_file_base_path + filename

        wb = xlrd.open_workbook(excel_file_path)
        sh = wb.sheet_by_index(0)

        sikdan = None
        for row in range(1, sh.nrows):
            row_values = sh.row_values(row)
            if row_values[0] == '식단':
                sikdan = {
                    'time': row_values[3],
                    'date': row_values[7],
                    'cafeteria': row_values[5],
                    'organization' : row_values[6],
                }
                ss = SikdanSerializer(data=sikdan)
                if ss.is_valid():
                    sikdan = ss.save()
                else :
                    print("\n\n****sikdan data invalid****\n")
                    print("organization_id="+row_values[6]+"cafeteria_id"+row_values[5])
                    print("\n"+row_values[3]+" "+row_values[7]+"\n")
                    exit()
            else :
                if sikdan == None:
                    print("\n\n****excel got somethin' wrong****\n")
                    exit()
                else :
                    # noinspection PyStatementEffect
                    dish = Dish.objects.filter(name=row_values[0], cafeteria=row_values[5])
                    if not dish.exists():
                        dish = {
                            'name': row_values[0],
                            'cafeteria': row_values[5],
                        }
                        ds = DishUpdateSerializer(data=dish)
                        if ds.is_valid():
                            dish = ds.save()
                        else :
                            print("\n\n****dish data invalid****\n")
                            exit()
                    else :
                        dish = dish.first()
                        dish.is_new = False
                        dish.frequency += 1
                    dish.sikdans.add(sikdan)
                    dish.save()
                    sikdan.dishes.add(dish)
                    sikdan.save()
        print('\nupdated sikdan successfully for '+str(filename)+'!!\n')