from datetime import datetime, date, timedelta
import calendar
from enum import Enum
from bs4 import BeautifulSoup

class WhichMonth(Enum):
    THIS = 1
    NEXT = 2
    OTHER = 3

def get_month_title_location(soup : BeautifulSoup):
    empty_cells : list = list()
    start_at = 0
    count = 0
    c = 0
    for row in soup.find_all('tr'):
        for cell in row.find_all('td'):
            c += 1
            if not cell.text.isdigit():
                empty_cells.append(c)
    starters = [x for x in empty_cells if x < 10]
    enders = [x for x in empty_cells if x > 10]
    if len(starters) > len(enders):
        start_at = starters[0]
        count = len(starters)
    else:
        start_at = enders[0]
        count = len(enders)
    return start_at, count

def main(which_month : WhichMonth):
    now : datetime = datetime.now()
    month_number = None
    year = None
    # month_full_name = None
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
        month_name = input("Which month calendar do you want? Type, at least, the first three letters of the month.\n")
        year = int(input("Which year?\n"))
        month_number = datetime.strptime(month_name, '%b').month

    soup = BeautifulSoup(calendar.HTMLCalendar().formatmonth(year, month_number), 'html.parser')
    (start_at, count) = get_month_title_location(soup)
    month_full_name = calendar.month_name[month_number]
    with open('month.html', 'w') as f:
        f.write(f'<html><head><title>{month_full_name}</title><link rel="stylesheet" href="month.css"></head><body>')
        f.write('<table>')
        f.write('<tr>')
        [f.write(f'<td class="dayoftheweek">{dotw}</td>') for dotw in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']]
        f.write('</tr>')

        c = 0
        for row in soup.find_all('tr'):
            f.write('<tr>')
            for cell in row.find_all('td'):
                c += 1
                if start_at <= c < start_at + count:
                    if c == start_at:
                        f.write(f'<td class="titletd" colspan="{count}">{month_full_name}<br>{year}</td>')
                    else:
                        continue
                else:
                    if (cell.text.isdigit()):
                        if date(year,month_number,int(cell.text)).weekday() > 4:
                            f.write(f'<td class="weekender">{cell.text}</td>')
                        else:
                            f.write(f'<td>{cell.text}</td>')
                    else:
                        f.write('<td>&nbsp;</td>')
            f.write('</tr>')
        f.write('</table>')
        f.write('</body></html>')
        print(f"Done - Created Month.html for {month_full_name}, {year}")

if __name__ == "__main__":
    now : datetime = datetime.now()
    print("Which month calendar do you want?")
    print(f"For this month's, type 1")
    print(f"For next month's, type 2")
    print(f"For any other month's, type 3")
    which_month = WhichMonth(int(input("")))
    main(WhichMonth(which_month))
