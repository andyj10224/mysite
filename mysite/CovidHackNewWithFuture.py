from pprint import pprint
import json
import os
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys

#Source: https://www.50states.com/abbreviations.htm
states_db = {
    'Alabama' : 'AL',
    'Alaska' : 'AK',
    'Arizona' : 'AZ',
    'Arkansas' : 'AR',
    'California' : 'CA',
    'Colorado' : 'CO',
    'Connecticut' : 'CT',
    'Delaware' : 'DE',
    'Florida' : 'FL',
    'Georgia' : 'GA',
    'Hawaii' : 'HI',
    'Idaho' : 'ID',
    'Illinois' : 'IL',
    'Indiana' : 'IN',
    'Iowa' : 'IA',
    'Kansas' : 'KS',
    'Kentucky' : 'KY',
    'Louisiana' : 'LA',
    'Maine' : 'ME',
    'Maryland' : 'MD',
    'Massachussetts' : 'MA',
    'Michigan' : 'MI',
    'Minnesota' : 'MN',
    'Mississippi' : 'MS',
    'Missouri' : 'MO',
    'Montana' : 'MT',
    'Nebraska' : 'NE',
    'Nevada' : 'NV',
    'New Hampshire' : 'NH',
    'New Jersey' : 'NJ',
    'New Mexico' : 'NM',
    'New York' : 'NY',
    'North Carolina' : 'NC',
    'North Dakota' : 'ND',
    'Ohio' : 'OH',
    'Oklahoma' : 'OK',
    'Oregon' : 'OR',
    'Pennsylvania' : 'PA',
    'Rhode Island' : 'RI',
    'South Carolina' : 'SC',
    'South Dakota' : 'SD',
    'Tennessee' : 'TN',
    'Texas' : 'TX',
    'Utah' : 'UT',
    'Vermont' : 'VT',
    'Virginia' : 'VA',
    'Washington' : 'WA',
    'West Virginia' : 'WV',
    'Wisconsin' : 'WI',
    'Wyoming' : 'WY',
    'District of Columbia' : 'DC',
    'Marshall Islands' : 'MH'

}

def covid_predict(folder, state):

    for root, dirs, files in os.walk(F'/home/ajiang10224/mysite/{folder}'):
        for filename in files:
            if '.csv' in filename:
                myfile = open(os.path.join(F'/home/ajiang10224/mysite/{folder}', filename), "r")

    header = myfile.readline()
    data = myfile.readlines()
    myfile.close()
    stateCount = 0
    newDict = {}

    header = header.strip("\n").split(",")

    deaths_mean = -1
    deaths_lower = -1
    deaths_upper = -1
    location_name = -1
    date_ind = -1

    for i in range(len(header)):
        if 'deaths_mean' in header[i]:
            deaths_mean = i
        elif 'deaths_lower' in header[i]:
            deaths_lower = i
        elif 'deaths_upper' in header[i]:
            deaths_upper = i
        elif 'location_name' in header[i]:
            location_name = i
        elif 'date' in header[i]:
            date_ind = i

    for aline in data:
        pieces = aline.strip("\n").split(",")
        if state in pieces[location_name]:
            stateCount += 1
            date = pieces[date_ind].strip('"')
            dayNumber = datetime.datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
            newDict[str(dayNumber)] = {'State': state, 'MeanDailyDeaths': pieces[deaths_mean], 'LowerBound': pieces[deaths_lower], 'UpperBound': pieces[deaths_upper]}

    print(json.dumps(newDict, indent = 4))
    #return ("Total number of entries: {}".format(stateCount))
    return newDict

def covid_actual(st):
    file = open("/home/ajiang10224/mysite/covid_deaths_usafacts.csv", "r")
    header = file.readline()
    data = file.readlines()
    file.close()

    header_pieces = header.strip("\n").split(",")

    newDict = {}

    for j in range(4, len(header_pieces)):
        if '/' in header_pieces[j][0:2]:
            dayNumber = datetime.datetime.strptime('0' + header_pieces[j], '%m/%d/%y').timetuple().tm_yday
        else:
            dayNumber = datetime.datetime.strptime(header_pieces[j], '%m/%d/%y').timetuple().tm_yday

        newDict[str(dayNumber)] = 0

        for aline in data:
            data_pieces = aline.strip("\n").split(",")
            if st in data_pieces[2]:
                if dayNumber == 22:
                    newDict[str(dayNumber)] += int(data_pieces[j])

                else:
                    newDict[str(dayNumber)] += int(data_pieces[j]) - int(data_pieces[j-1])

    print(json.dumps(newDict, indent = 4))
    return newDict


#print(covid_predict("Georgia"))
#print(covid_actual("ga"))

def covid_writer(folder, state):
    predictDict = covid_predict(folder, state)
    actualDict = covid_actual(states_db[state])

    compareFile = open(F'/home/ajiang10224/mysite/static/graphs/{folder}_{state}_with_future.csv', 'w+')

    compareFile.write("DayOfYear,ActualDeaths,EstimatedLow,EstimatedMean,Estimated High\n")

    for key, value in predictDict.items():
        if key in actualDict.keys():
            compareFile.write(F"{key},{actualDict[key]},{value['LowerBound']},{value['MeanDailyDeaths']},{value['UpperBound']}\n")

        else:
           compareFile.write(F"{key},N/A,{value['LowerBound']},{value['MeanDailyDeaths']},{value['UpperBound']}\n")

    compareFile.close()

def graph_maker(folder, state):
    compareFile = open(F'/home/ajiang10224/mysite/static/graphs/{folder}_{state}_with_future.csv', 'r')

    header = compareFile.readline()
    data = compareFile.readlines()

    compareFile.close()

    for i in range(len(data)):
        data[i] = data[i].strip("\n").split(",")

    # data = np.array(data, dtype=float)

    print(data)

    dayOfYear = []
    dayOfYearNoFuture = []
    actualDeaths = []
    actualDeathsNoNA = []
    estimatedLow = []
    estimatedMean = []
    estimatedHigh = []

    for x in data:
        dayOfYear.append(float(x[0]))
        actualDeaths.append(x[1])
        estimatedLow.append(float(x[2]))
        estimatedMean.append(float(x[3]))
        estimatedHigh.append(float(x[4]))

    for i in range(len(actualDeaths)):
        if 'N/A' not in actualDeaths[i]:
            actualDeathsNoNA.append(float(actualDeaths[i]))
            dayOfYearNoFuture.append(dayOfYear[i])

    print(actualDeathsNoNA)

    plt.plot(dayOfYearNoFuture, actualDeathsNoNA, label='actual deaths')
    plt.plot(dayOfYear, estimatedMean, label='estimated mean')
    plt.plot(dayOfYear, estimatedLow, '--', label='estimated low')
    plt.plot(dayOfYear, estimatedHigh, '--', label='estimated high')
    plt.legend()

    plt.xlabel("Days Into The Year")
    plt.ylabel("Deaths from COVID-19")

    plt.savefig(F'/home/ajiang10224/mysite/static/graphs/{folder}_{state}_with_future.png')

    plt.close('all')

def main(argv=sys.argv):
    args = argv
    covid_writer(args[1], args[2])
    graph_maker(args[1], args[2])

if __name__ == '__main__':
    main()
