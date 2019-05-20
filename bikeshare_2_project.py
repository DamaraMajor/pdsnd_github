import time
import csv
import pandas as pd
import numpy as np
from os import system, name

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']

def screen_clear():
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    def city():
        while True:
            city_input = input('Which city would you like to learn about? Chicago, New York City, or Washington?\n\nSelection: ').lower()
            if city_input not in CITY_DATA.keys():
                print('\nI didn\'t understand your response.\n')
            else:
                city = city_input
                print(f'Thank you. I will now present you with data for {city_input.title()}.\n')
                return city

    def month():
        while True:
            month_input = input('We have data for January through June. Which month would you like data for (or you can select all)? ').title()
            if month_input not in months and month_input != 'All':
                print('I did not understand your response. Please type a month or select all.\n')
            else:
                month = month_input
                return month

    # get user input for day of week (all, monday, tuesday, ... sunday)
    def day():
        while True:
            day_input = input('Which weekday would you would like data for (or you can select all)? ').title()
            weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if day_input not in weekdays and day_input != 'All':
                print('I did not understand your response. Please type a weekday or select all.\n')
            else:
                day = day_input
                return day

    print('-'*40)
    return city(), month(), day()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    # for city in CITY_DATA:
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    #
    # # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    #
    print('Most Frequent Month of Travel: ', popular_month)
    print('Most Frequent Day of Travel: ', popular_day)
    print('Most Frequent Hour of Travel: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Start End'] = list(zip(df['Start Station'], df['End Station']))

    paired_start_end = df['Start End'].mode()[0]

    print('Most Commonly Used Start Station: ', popular_start_station)
    print('Most Commonly Used End Station: ', popular_end_station)
    print('Most Commonly Paired Start and End Station:\n',paired_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_sec = df['Trip Duration'].sum()
    def total_travel(seconds):
        d = seconds//86400
        h = (seconds - d*86400)//(60*60)
        m = (seconds - (d*86400) - (h*60*60))//60
        s = (seconds - (d*86400) - (h*60*60) - (m*60))
        return('days: {}, hours: {}, minutes: {}, seconds: {}'.format(d, h, m, s))

    # display mean travel time
    average_travel_sec = df['Trip Duration'].mean()
    def average_travel(seconds):
        h = seconds//(60*60)
        m = (seconds-h*60*60)//60
        s = seconds-(h*60*60)-(m*60)
        return('minutes: {}, seconds: {}'.format(m, s))

    print('Total Time Spent Traveling: ', total_travel(total_travel_sec),'\n')
    print('Average Length of Trip: ', average_travel(average_travel_sec),'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    # Display counts of gender
    #chicago and new_york_city only
    def gender():
        if df.columns.isin(['Gender']).any():
            print('Total of each gender:\n', df['Gender'].value_counts(),'\n')
        else:
            print('Total of each gender:\nThis data was not collected for this city\n')
    # Display earliest, most recent, and most common year of birth
    #chicago and new_york_city only
    def birth_year():
        if df.columns.isin(['Birth Year']).any():
            print('Earliest Birth Year:\n', int(df['Birth Year'].min()))
            print('Most Recent Birth Year:\n', int(df['Birth Year'].max()))
            print('Most Common Birth Year:\n', int(df['Birth Year'].mode()[0]),'\n')
        else:
            print('Birth Year:\nThis data was not collected for this city\n')

    print('Total of each user type:\n',user_type,'\n')

    gender()

    birth_year()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def countdown(t):
    print('Seconds until next set of data displays:')
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

def main():
    screen_clear()
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        countdown(5)
        screen_clear()
        station_stats(df)
        countdown(5)
        screen_clear()
        trip_duration_stats(df)
        countdown(5)
        screen_clear()
        user_stats(df)
        countdown(5)
        screen_clear()

        while True:
            print(df.head())
            more_data = input('Would you like to see more data? Enter yes or no: ')
            if more_data == 'yes':
                df.drop(df.index[:5], inplace=True)
                print(df.head())
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
