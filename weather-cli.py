import csv

fields = rows = []
at = mint = maxt = ht = wd = ""


# ------------------------------------------------------------------------------------------------------------------
# import: Import raw weather data from a text file.
# ------------------------------------------------------------------------------------------------------------------
def imp_csv_data():
    filename = "weather.csv"

    with open(filename, "r") as csvfile:  # open csv file
        csvreader = csv.reader(csvfile)  # make a csv reader
        global fields
        # assigning the current row to fields[] and moving reader to next row
        fields = next(csvreader)

        # iterating through remaining rows of csv file & append as a list in rows[]
        for row in csvreader:
            rows.append(row)


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
    # for r in row:
    #     print(r)

    filename = "results.csv"

    with open(filename, "w") as csvfile:  # writing to csv file
        csvwriter = csv.writer(csvfile)  # creating a csv writer object
        csvwriter.writerow(fields)  # writing the fields
        csvwriter.writerow(row)  # writing the data rows


# ------------------------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    imp_csv_data()
    sahi = True
    sahi = stat(1, 10)
    if sahi is True:
        exp_csv_data()
    else:
        print("The range of days is from 1 to 365.")
# ------------------------------------------------------------------------------------------------------------------
#                   NOTES:
# will convert dates in user inputs to the day number (1-365)
