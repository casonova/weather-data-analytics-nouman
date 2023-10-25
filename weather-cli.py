import csv
import os
from datetime import date
import argparse
import logging
import matplotlib.pyplot as plt

fields = rows = []
at = mint = maxt = ht = wd = ""
mins = []
maxs = []

st_date = ed_date = ""

# ------------------------------------------------------------------------------------------------------------------
# Logger configurations:
# ------------------------------------------------------------------------------------------------------------------
# Create and configure logger
logging.basicConfig(
    filename="file.log", format="%(asctime)s %(levelname)s %(message)s", filemode="a"
)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


# ------------------------------------------------------------------------------------------------------------------
# import: Import raw weather data from a text file.
# ------------------------------------------------------------------------------------------------------------------
def imp_csv_data(file):
    # filename = "weather.csv"

    if os.path.isfile(file) is True:
        with open(file, "r") as csvfile:  # open csv file
            csvreader = csv.reader(csvfile)  # make a csv reader
            global fields, rows
            # assigning the current row to fields[] and moving reader to next row
            fields = next(csvreader)

            # iterating through remaining rows of csv file & append as a list in rows[]
            for row in csvreader:
                rows.append(row)
        logger.info(f"{file} imported.")
        return True
    else:
        logger.error(f"{file} not found!")
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
    logger.info("avg called.")
    return float("{:.2f}".format((avg_min(st, ed) + avg_max(st, ed)) / 2))


def min_temp(st, ed):
    global mins
    for row in rows[(st - 1) : ed]:
        for col in row[:1]:
            mins.append(float(col))

    logger.info("min_temp called.")
    return min(mins)


def max_temp(st, ed):
    global maxs
    for row in rows[(st - 1) : ed]:
        for col in row[1:2]:
            maxs.append(float(col))

    logger.info("max_temp called.")
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
    logger.info("hum_trend called.")
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
    logger.info("max_wind_day called.")
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

    logger.info(f"Average Temperature: {at}")
    logger.info(f"Minimum Temperature: {mint}")
    logger.info(f"Maximum Temperature: {maxt}")
    logger.info(f"Humidity Trend: {ht}")
    logger.info(f"Windy Day: {wd}")

    return True


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

    logger.info(f"Results exported in {filename}")


# ------------------------------------------------------------------------------------------------------------------
# export raw data to a CSV file to verify proper functioning of import command.
# ------------------------------------------------------------------------------------------------------------------
def exp_raw_data():
    filename = "raw_sample.csv"

    with open(filename, "w", newline="") as csvfile:  # writing to csv file
        csvwriter = csv.writer(csvfile)  # creating a csv writer object
        csvwriter.writerow(fields)  # writing the fields
        for row in rows[:5]:
            csvwriter.writerow(row)  # writing the data rows
    logger.info(f"Sample raw data exported in {filename}")


# ------------------------------------------------------------------------------------------------------------------
# 1- Bonus:
# Implement additional analytics features, like identifying patterns or anomalies in the weather data.
# Use a data visualization library to generate graphs based on the analytics:
# ------------------------------------------------------------------------------------------------------------------
def plotting():
    plt.plot(mins, label="Minimum Temperature")
    plt.plot(maxs, label="Maximum Temperature")
    plt.title(f"Temperature Analysis in range {st_date} to {ed_date}")
    plt.legend()
    plt.savefig("plot")


# ------------------------------------------------------------------------------------------------------------------
# CLI Commands implementation:
# ------------------------------------------------------------------------------------------------------------------
def numOfDays(date1, date2):
    # check which date is greater to avoid days output in -ve number
    if date2 > date1:
        return (date2 - date1).days
    else:
        return (date1 - date2).days


def cli_comm():
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
            exp_raw_data()
            print(
                '"% s" imported successfully. You can check sample data in raw_sample.csv'
                % args.file
            )
        else:
            print("% s not present." % args.file)

    if args.range:
        date_range = str(args.range).split(" to ")
        global st_date, ed_date
        st_date = date_range[0]
        ed_date = date_range[1]

        # difference of both dates from 2023-01-01
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
            plotting()
        else:
            print("The range of date is from 2023-01-01 to 2023-12-31")
        
    # if args.format:
    #     print("% s exported successfully." % args.format)


# ------------------------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    cli_comm()
# ------------------------------------------------------------------------------------------------------------------
#                   NOTES:
# will convert dates in user inputs to the day number (1-365)
