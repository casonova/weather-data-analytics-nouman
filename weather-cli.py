import csv

fields = rows = []
at = mint = maxt = ht = wd = ""


# ------------------------------------------------------------------------------------------------------------------
# import: Import raw weather data from a text file.
# ------------------------------------------------------------------------------------------------------------------
def imp_csv_data(file):
    # filename = "weather.csv"
    import os

    if os.path.isfile(file) is True:
        with open(file, "r") as csvfile:  # open csv file
            csvreader = csv.reader(csvfile)  # make a csv reader
            global fields, rows
            # assigning the current row to fields[] and moving reader to next row
            fields = next(csvreader)

            # iterating through remaining rows of csv file & append as a list in rows[]
            for row in csvreader:
                rows.append(row)

        return True
    else:
        return False


# ------------------------------------------------------------------------------------------------------------------
# analyze: Perform analytics on the imported data.
# ------------------------------------------------------------------------------------------------------------------
def avg_min(st, ed):  # 1-10 total range (1-366)
    avg_min_t = 0
    for row in rows[(st - 1) : ed]:
        for col in row[:1]:
            avg_min_t += float(col)

    avg_min_t /= 10
    return avg_min_t


def avg_max(st, ed):  # 1-10 total range (1-366)
    avg_max_t = 0
    for row in rows[(st - 1) : ed]:
        for col in row[1:2]:
            avg_max_t += float(col)

    avg_max_t /= 10
    return avg_max_t


def avg(st, ed):  # 1-10 total range (1-366)
    # return (avg_min(st, ed) + avg_max(st, ed)) / 2
    # float("{:.2f}".format(x))
    return float("{:.2f}".format((avg_min(st, ed) + avg_max(st, ed)) / 2))


def min_temp(st, ed):
    mins = []
    for row in rows[(st - 1) : ed]:
        for col in row[:1]:
            mins.append(float(col))

    return min(mins)


def max_temp(st, ed):
    maxs = []
    for row in rows[(st - 1) : ed]:
        for col in row[1:2]:
            maxs.append(float(col))

    return max(maxs)


def hum_trend(st, ed):
    hum1 = []
    hum2 = []
    mid = (ed - st) / 2
    count = 0

    for row in rows[(st - 1) : ed]:
        for col in row[11:12]:
            if count <= mid:
                hum1.append(float(col))
                count += 1
            else:
                hum2.append(float(col))

    hum1 = sum(hum1) / len(hum1)
    hum2 = sum(hum2) / len(hum2)
    if hum1 > hum2:
        return "Decreasing"
    elif hum1 < hum2:
        return "Increasing"
    else:
        return "Stable"


def max_wind_day(st, ed):
    max_wind = []  # get wind speeds of required range
    for row in rows[(st - 1) : ed]:  # iterate into required rows
        for col in row[9:10]:  # limiting the fields/ col(s)
            if col != "NA":
                max_wind.append(float(col))  # appending rows data
            else:
                max_wind.append(0)  # appending rows data

    r_id = max_wind.index(max(max_wind))  # getting the result index
    r_id += st - 1  # w.r.t given range
    # return date and day of the r_id
    return str(rows[r_id][22:23])[2:-2]


def stat(st, ed):
    if st < 1 or ed > 365:
        return False
    global at, mint, maxt, ht, wd  # update global variables
    at = str(avg(st, ed))
    mint = str(min_temp(st, ed))
    maxt = str(max_temp(st, ed))
    ht = hum_trend(st, ed)
    wd = max_wind_day(st, ed)

    return True

    # print("Average Temperature: " + at)
    # print("Minimum Temperature: " + mint)
    # print("Maximum Temperature: " + maxt)
    # print("Humidity Trend: " + ht)
    # print("Windy Day: " + wd)


# ------------------------------------------------------------------------------------------------------------------
# export: Export the analytics results to a text or CSV file.
# ------------------------------------------------------------------------------------------------------------------
def exp_csv_data():
    fields = [
        "Average Temperature",
        "Minimum Temperature",
        "Maximum Temperature",
        "Humidity Trend",
        "Windy Day",
    ]
    row = [at, mint, maxt, ht, wd]
    filename = "results.csv"

    with open(filename, "w") as csvfile:  # writing to csv file
        csvwriter = csv.writer(csvfile)  # creating a csv writer object
        csvwriter.writerow(fields)  # writing the fields
        csvwriter.writerow(row)  # writing the data rows


# ------------------------------------------------------------------------------------------------------------------
# Logging: Log every action, such as importing data, performing calculations, and exporting results.
# ------------------------------------------------------------------------------------------------------------------
def exp_csv_log(stat):
    fields = ["Datetime", "Import File", "Export File", "Status"]

    from datetime import datetime

    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    if stat is True:
        row = [now, "weather.csv", "results.csv", "Success"]
    else:
        row = [now, "weather.csv", "results.csv", "Failure: reason"]

    filename = "log.csv"

    import os

    with open(filename, "a", newline="") as csvfile:  # writing to csv file
        csvwriter = csv.writer(csvfile)  # creating a csv writer object
        if os.stat("log.csv").st_size == 0:
            csvwriter.writerow(fields)  # writing the fields
            csvwriter.writerow(row)  # writing the data rows
        else:
            csvwriter.writerow(row)  # writing the data rows


# ------------------------------------------------------------------------------------------------------------------
# CLI Commands implementation:
# python weather_cli.py import --file raw_weather_data.txt
# python weather_cli.py analyze --range "2023-01-01 to 2023-01-31"
# python weather_cli.py export --format csv
# ------------------------------------------------------------------------------------------------------------------
def numOfDays(date1, date2):
    # check which date is greater to avoid days output in -ve number
    if date2 > date1:
        return (date2 - date1).days
    else:
        return (date1 - date2).days


def cli_comm():
    import argparse

    # Initialize parser
    parser = argparse.ArgumentParser()

    m1 = "Usage: python weather-cli.py --file weather.csv"
    m2 = 'Usage: python weather-cli.py --range "2023-01-01 to 2023-01-31"'
    # m3 = "Usage: python weather-cli.py --format csv"

    # Adding optional argument
    # parser.add_argument("-o", "--inppp", help="Show Output")
    parser.add_argument("-f", "--file", help=m1)
    parser.add_argument("-r", "--range", help=m2)
    # parser.add_argument("-e", "--format", help=m3)

    # Read arguments from command line
    args = parser.parse_args()

    if args.file:
        if imp_csv_data(args.file) is True:
            print('"% s" imported successfully.' % args.file)
        else:
            print("% s not present." % args.file)

    if args.range:
        date_range = str(args.range).split(" to ")
        st_date = date_range[0]
        ed_date = date_range[1]
        # difference of both dates from 2023-01-01
        from datetime import date

        Y1, M1, D1 = st_date.split("-")
        Y2, M2, D2 = ed_date.split("-")
        date0 = date(2023, 1, 1)
        date1 = date(int(Y1), int(M1), int(D1))
        date2 = date(int(Y2), int(M2), int(D2))
        st = numOfDays(date0, date1)
        ed = numOfDays(date1, date2)
        sahi = True
        sahi = stat(st + 1, ed + 1)
        if sahi is True:
            print("% s, range analysed successfully." % args.range)
            exp_csv_data()
        else:
            print("The range of date is from 2023-01-01 to 2023-12-31")
        exp_csv_log(sahi)

    # if args.format:
    #     print("% s exported successfully." % args.format)


# ------------------------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    cli_comm()

    # imp_csv_data()
    # sahi = True
    # sahi = stat(1, 36)
    # if sahi is True:
    #     exp_csv_data()
    # else:
    #     print("The range of days is from 1 to 365.")
    # exp_csv_log(sahi)
# ------------------------------------------------------------------------------------------------------------------
#                   NOTES:
# will convert dates in user inputs to the day number (1-365)
