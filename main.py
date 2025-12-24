from datetime import datetime, date, timedelta
import calendar
from enum import Enum
from bs4 import BeautifulSoup
from math import isnan

class WhichMonth(Enum):
    THIS = 1
    NEXT = 2
    OTHER = 3

def main(which_month : WhichMonth):
    now : datetime = datetime.now()
    month_number = None
    year = None
    if which_month == WhichMonth.THIS:
        month_number = now.month
        year = now.year
    elif which_month == WhichMonth.NEXT:
        today = date.today()
        first_of_this_month = today.replace(day=1)
        next_month = first_of_this_month + timedelta(days=32)
        month_number = next_month.month
        year = next_month.year
    elif which_month == WhichMonth.OTHER:
        month_name = input("Which month calendar do you want?\nType, at least, the first three letters of the month.\n")
        year = int(input("Which year?\n"))
        month_number = datetime.strptime(month_name, '%b').month
        print(datetime.strptime(month_name, '%b'))

    soup = BeautifulSoup(calendar.HTMLCalendar().formatmonth(year, month_number), 'html.parser')
    
    with open('month.html', 'w') as f:
        f.write('<html><head><link rel="stylesheet" href="month.css"></head><body>')
        f.write('<table>')
        for row in soup.find_all('tr'):
            f.write('<tr>')
            for cell in row.find_all('td'):
                if (cell.text.isdigit()):
                    f.write(f'<td>{cell.text}</td>')
                else:
                    f.write(f'<td>&nbsp;</td>')
            f.write('</tr>')
        f.write('</table>')
        f.write('</body></html>')

if __name__ == "__main__":
    now : datetime = datetime.now()
    print("Which month calendar do you want?")
    print(f"For this month's, type 1")
    print(f"For next month's, type 2")
    print(f"For any other month's, type 3")
    try:
        which_month = WhichMonth(int(input("")))
        main(WhichMonth(which_month))
    except ValueError:
        print("Please enter a valid input")
