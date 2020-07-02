# ------------ COVID-19 World Data Amalyzer ---------------
# This program shows the user with all the required data related to the COVID-9 cases of a country
# It also compares the data between two countries

# ========= Importing Important Libraries ========= #
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import sys
import json
import urllib
# ========= Comparison Class That Compares Data of Two Countries ========= #


class Comparison:

    def country_data(self, name, statistic, in_start_date, in_end_date):
        url = get_url(name)
        try:    # if some problem exists it show's the warning message
            data = urllib.request.urlopen(url).read()
            country_data = json.loads(data)
        except:
            print("Something Went Wrong. Check Your Internet Connection And Try Again.")
            sys.exit()
        if len(country_data) == 0:
            print("No Data Exist For This Country")
            self.main()
        else:
            return self.read_data(country_data, statistic, in_start_date, in_end_date)

    # This function reads the required data from the url extracted from the above function
    def read_data(self, data, statistic, start_date, end_date):
        dates = []
        count = []
        for country in data:
            for key, value in country.items():
                if key.lower() == statistic:
                    country_date = country['Date']
                    date = country_date.split("T", maxsplit=9)[0].replace('-', '')
                    if (int(date) >= start_date) and (int(date) <= end_date):  # and date is between range
                        if country[statistic.capitalize()] is not None:  # only if there are some numbers present
                            dates.append(int(date))
                            count.append(country[statistic.capitalize()])
                        elif country[statistic] is None:  # if the value is null, do nothing
                            pass
        dates = list(dict.fromkeys(dates))
        print(dates)
        print(count)
        return dates, count

    # This function displays the data on the graphs as well as terminal
    def display_data(self, dates, country_1_count, country_1_name, country_2_count, country_2_name, statistic):
        print("Displaying Data for the Statistic " + statistic.capitalize())
        print("Date".ljust(20) + country_1_name.ljust(20).capitalize() + country_2_name.ljust(20).capitalize())
        for date, c1, c2 in zip(dates, country_1_count, country_2_count):
            print(str(date).ljust(20) + str(c1).ljust(20) + str(c2).ljust(20))

        x = np.arange(len(dates))
        width = 0.25
        fig, ax = plt.subplots()
        ax.bar(x, country_1_count, width, color='green', label=country_1_name.capitalize())
        ax.bar(x + width, country_2_count, width, color='orange', label=country_2_name.capitalize())

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Cases')
        ax.set_title('Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(dates, rotation='vertical')
        ax.legend()
        fig.tight_layout()
        plt.show()

        self.re_analyze()
    # This function is asking the user if he wants another analysis or not
    def re_analyze(self):
        re_analysis = input("Perform another analysis (yes/no)? ")
        if re_analysis.lower() == 'yes':
            main()
        elif re_analysis.lower() == 'no':
            sys.exit()
        else:
            print("Kindly Enter Correct Choice")
            self.re_analyze()

    # This is the main function of this class handling all the function in it
    def main(self):
        print("""
    Instructions:
    - You Can Always Check Exact Name of a Country by Selecting Option 1 from Main Menu
    - Kindly Enter Full Name of Country
    - Kindly Give Spaces in Name (e.g United States of America)
    - Don't Use Abbreviated Names (e.g Use United States of America instead of USA)
        """)
        # Taking Inputs from the user
        country_1 = input("Enter Name of First Country: ")
        country_2 = input("Enter Name of Second Country: ")
        for v in range(100):
            in_statistic = input("Which statistic would you like to search?[Confirmed/Deaths/Recovered] ")
            statistic_list = ['confirmed', 'deaths', 'recovered']
            if in_statistic.lower() in statistic_list:
                statistic = in_statistic.lower()
                break
            else:
                print("Please Choose Right Statistic\n")
        in_start = input("Would you like to add a start date (yes/no)? ")
        if in_start.lower() == 'yes':
            try:
                in_start_date = int(input("Which start date would you like to use (YYYYMMDD)? "))
            except ValueError:
                print("You Entered Wrong Date. Results will be shown from beginning")
                in_start_date = -99999999
        elif in_start.lower() == 'no':
            in_start_date = -99999999
        else:
            print("You Entered Wrong Choice. Results will be shown from beginning")
            in_start_date = -99999999

        in_end = input("Would you like to add an end date (yes/no)? ")
        if in_end.lower() == 'yes':
            try:
                in_end_date = int(input("Which end date would you like to use (YYYYMMDD)?"))
            except ValueError:
                print("You Entered Wrong Date. Results will be shown until today")
                in_end_date = 99999999
        elif in_end.lower() == 'no':
            in_end_date = 99999999
        else:
            print("You Entered Wrong Choice. Results will be shown until today")
            in_end_date = 99999999
        # the functions are called and required outputs are gained from them

        dates_1, country_1_count = self.country_data(country_1, statistic, in_start_date, in_end_date)
        dates_2, country_2_count = self.country_data(country_2, statistic, in_start_date, in_end_date)
        self.display_data(dates_1, country_1_count, country_1, country_2_count, country_2, statistic)

# ========= Single Country Data Class That Display Data of One Country ========= #


class SingleCountryData:

    def single_country_data(self, name,statistic, in_start_date, in_end_date, graph):
        url = get_url(name)
        try:
            data = urllib.request.urlopen(url).read()
            country_data = json.loads(data)
        except:
            print("Can't Get Required Data Currently. Check Your Internet Connection And Try Again.")
            sys.exit()
        if len(country_data) == 0:
            print("No Data Exist For This Country")
            self.main()
        else:
            self.read_data(country_data, statistic, in_start_date, in_end_date, graph)

    def read_data(self, data, statistic, start_date, end_date, graph):
        dates = []                                          # This list stores dates
        count = []                                          # This list stores the count of statistic if given
        deaths = []                                         # This list stores death count if statistic is not given
        confirmed = []                                      # This list stores confirmed count if statistic is not given
        recovered = []                                      # This list stores recovered count if statistic is not given
        for country in data:
            if statistic != 'all':
                for key, value in country.items():
                    if key.lower() == statistic:
                        country_date = country['Date']
                        date = country_date.split("T", maxsplit=9)[0].replace('-', '')
                        if (int(date) >= start_date) and (int(date) <= end_date):  # and date is between range
                            if country[statistic.capitalize()] is not None:  # only if there are some numbers present
                                dates.append(int(date))
                                count.append(country[statistic.capitalize()])
                            elif country[statistic] is None:  # if the value is null, do nothing
                                pass
            elif statistic == 'all':
                for key, value in country.items():
                    country_date = country['Date']
                    date = country_date.split("T", maxsplit=9)[0].replace('-', '')
                    if (int(date) >= start_date) and (int(date) <= end_date):  # and date is between range
                        if key == 'Confirmed':
                            if country[key] is not None:  # only if there are some numbers present
                                dates.append(int(date))
                                confirmed.append(country[key])
                            elif country[statistic] is None:  # if the value is null, do nothing
                                pass
                        elif key == 'Deaths':
                            if country[key] is not None:  # only if there are some numbers present
                                dates.append(int(date))
                                deaths.append(country[key])
                            elif country[statistic] is None:  # if the value is null, do nothing
                                pass
                        elif key == 'Recovered':
                            if country[key] is not None:  # only if there are some numbers present
                                dates.append(int(date))
                                recovered.append(country[key])
                            elif country[statistic] is None:  # if the value is null, do nothing
                                pass
        dates = list(dict.fromkeys(dates))
        self.display_data(dates, count,deaths,confirmed,recovered,statistic,graph)

    def display_data(self, dates, count, deaths, confirmed, recovered, statistic, graph):
        if graph:                       # If the user wants to show data on graph this condition
            if statistic != 'all':      # turn true and following code will execute
                y_pos = np.arange(len(dates))
                plt.bar(y_pos, count, align='center', alpha=0.5)
                plt.xticks(y_pos, dates, rotation='vertical', ha="right")
                plt.ylabel(statistic.upper())
                plt.xlabel("DATES")
                # plt.title("Cases between " + str(dates[0]) + " and " + str(dates[-1]))
                plt.show()
                print("Date\t\t\t" + statistic.capitalize())
                for date, count in zip(dates, count):
                    print(str(date)+"\t\t\t"+str(count))
            if statistic == 'all':
                x = np.arange(len(dates))  # the label locations
                width = 0.25  # the width of the bars

                fig, ax = plt.subplots()
                ax.bar(x-width, deaths, width,color='red', label='Deaths')
                ax.bar(x, recovered, width,color='green', label='Recovered')
                ax.bar(x+width, confirmed, width, color='orange', label='Confirmed')

                # Add some text for labels, title and custom x-axis tick labels, etc.
                ax.set_ylabel('Cases')
                ax.set_title('Comparison')
                ax.set_xticks(x)
                ax.set_xticklabels(dates, rotation='vertical')
                ax.legend()
                fig.tight_layout()
                plt.show()
                print("Date".ljust(20)+"Confirmed".ljust(20)+"Recovered".ljust(20)+"Deaths".ljust(20))
                for date, confirm, recover, death in zip(dates,confirmed,recovered,deaths):
                    print(str(date).ljust(20) + str(confirm).ljust(20) + str(recover).ljust(20) + str(death).ljust(20))
        else:
            if statistic != 'all':
                print("Date\t\t\t" + statistic.capitalize())
                for date, count in zip(dates, count):
                    print(str(date)+"\t\t\t"+str(count))
            if statistic == 'all':
                print("Date".ljust(20)+"Confirmed".ljust(20)+"Recovered".ljust(20)+"Deaths".ljust(20))
                for date, confirm, recover, death in zip(dates,confirmed,recovered,deaths):
                    print(str(date).ljust(20) + str(confirm).ljust(20) + str(recover).ljust(20) + str(death).ljust(20))

        self.re_analyze()

    def re_analyze(self):               # This function provides option to exit or re-analyze data
        re_analysis = input("Perform another analysis (yes/no)? ")
        if re_analysis.lower() == 'yes':
            main()
        elif re_analysis.lower() == 'no':
            sys.exit()
        else:
            print("Kindly Enter Correct Choice")
            self.re_analyze()

    def main(self):
        print("""
Instructions:
    - You Can Always Check Exact Name of a Country by Selecting Option 1 from Main Menu
    - Kindly Enter Full Name of Country
    - Kindly Give Spaces in Name (e.g United States of America)
    - Don't Use Abbreviated Names (e.g Use United States of America instead of USA)
        """)
        name = input("Enter Name of the Country: ")
        in_statistic = input("Which statistic would you like to search?[Confirmed/Deaths/Recovered] ")
        statistic_list = ['confirmed', 'deaths', 'recovered']
        if in_statistic.lower() in statistic_list:
            statistic = in_statistic.lower()
        else:
            print("You Entered Wrong Statistic. All Statistics Will Be Shown")
            statistic = "all"
        in_start = input("Would you like to add a start date (yes/no)? ")
        if in_start.lower() == 'yes':
            try:
                in_start_date = int(input("Which start date would you like to use (YYYYMMDD)? "))
            except ValueError:
                print("You Entered Wrong Date. Results will be shown from beginning")
                in_start_date = -99999999
        elif in_start.lower() == 'no':
            in_start_date = -99999999
        else:
            print("You Entered Wrong Choice. Results will be shown from beginning")
            in_start_date = -99999999

        in_end = input("Would you like to add an end date (yes/no)? ")
        if in_end.lower() == 'yes':
            try:
                in_end_date = int(input("Which end date would you like to use (YYYYMMDD)?"))
            except ValueError:
                print("You Entered Wrong Date. Results will be shown until today")
                in_end_date = 99999999
        elif in_end.lower() == 'no':
            in_end_date = 99999999
        else:
            print("You Entered Wrong Choice. Results will be shown until today")
            in_end_date = 99999999
        in_graph = input("Do You Want To Display Data on a Graph?(yes/no)")
        if in_graph.lower() == 'yes':
            graph = True
        elif in_graph.lower() == 'no':
            graph = False
        else:
            print("You Entered Wrong Choice. No Graphs Will Be Shown")
            graph = False
        self.single_country_data(name, statistic, in_start_date, in_end_date, graph)

# ========= Country List Class That Displays Exact Names of The Countries ========= #


class CountryList:
    def country_list(self):
        with open('countries.json') as f:
            slug_data = json.load(f)
        i = 1
        for count in slug_data:
            for k, v in count.items():
                if k == 'Country':
                    print(str(i)+"."+v)
                    i += 1
        main()


def get_url(country):   # This function gives back the url having covid-19 data of the required country
    condition = True
    with open('countries.json') as f:
        slug_data = json.load(f)
    slug = ''
    while condition:
        for count in slug_data:
            for k, v in count.items():
                if k == 'Country' and ''.join(v.split()).lower() == ''.join(country.split()).lower():
                    for key, value in count.items():
                        if key == 'Slug':
                            slug = value
                            condition = False
        condition = False
    if slug == '':
        print("\t\t\t\tWARNING: Country Do Not Exist")
        kjh = SingleCountryData()
        kjh.main()
    else:
        url = "https://api.covid19api.com/total/country/" + str(slug)
        return url


def main():     # ******** MAIN FUNCTION THAT IS CONTROLLING WHOLE PROGRAM ********** #
    print("Kindly Select One of the Given Options")
    try:
        print("""
                     1. List of Names of Countries
                     2. Comparison Between Two Countries' Cases
                     3. Data of a Single Country
                     4. Exit 
                     """)
        user_input = int(input("Enter Your Selection: "))
    except ValueError:
        print("You Entered Wrong Value")
        sys.exit()
    input_list = [1, 2, 3, 4]
    if user_input in input_list:
        value = user_input
    else:
        print("\n\n\n\nWARNING: Wrong Selection\n")
        main()
    if value == 1:
        obj = CountryList()
        obj.country_list()
    elif value == 3:
        scd = SingleCountryData()
        scd.main()
    elif value == 2:
        cp = Comparison()
        cp.main()
    elif value == 4:
        sys.exit()

# This is where the execution starts
if __name__ == "__main__":
    print("\n\n\n\n\n\n")
    print("------------------------------------------  COVID-19 ANALYZER  ------------------------------------------")
    main()



