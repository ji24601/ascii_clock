import datetime
import time

t=time.localtime()
Y=str(t.tm_year)
M=str(t.tm_mon)


def getMonthName(month):
    li = ['January', 'February', 'March', 'April', 'May', 'June',

          'July', 'August', 'Setember', 'October', 'November', 'December']

    monthName = li[month - 1]

    return monthName


def title(year, month):
    print('    ', getMonthName(month), ' ', year)

    print('-' * 50)

    print('일  월  화  수  목  금  토')


def getStartDay(year, month):
    d = datetime.date(year, month, 1)

    return d.weekday()  # 월요일 0


def getLastDay(year, month):
    if month == 12:

        year = year + 1

        month = 1

    else:

        month = month + 1

    d = datetime.date(year, month, 1)

    t = datetime.timedelta(days=1)

    k = d - t

    return k.day


def body(year, month):
    startday = getStartDay(year, month)

    lastday = getLastDay(year, month)

    if startday == 6:

        s = 1

    else:

        s = startday + 2

    c = 0

    m = 0

    for k in range(6):

        for i in range(7):

            c = c + 1

            if c < s:

                print('{:>2}'.format(' '), end='  ')

            else:

                if lastday > m:
                    m = m + 1

                    print('{:>2}'.format(m), end='  ')

        print()


def Dal(year, month):
    title(year, month)

    body(year, month)


def main():
    year = eval(Y)

    month = eval(M)

    Dal(year, month)


main()
