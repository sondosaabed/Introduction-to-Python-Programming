#####
##### Sondos Aabed Explores the Bokeshare Dataset
#####

### Importing the necessary libraries
import time
import pandas as pd
import numpy as np

#### this is the csv files dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#### in this method get the filters inputted by the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    #####
    # In those cases an invalid input is handled by asking the user to try again until it's true input
    ####
    # get user input for city (chicago, new york city, washington). 
    while True:
        city= input("\n Which City would like to explore? All, Chicago, New york city, Or Washington?\n")
        city=city.lower()
        if city not in ('all', 'new york city', 'chicago','washington'):
            print("Try to enter another city that is either: Chicago, New york city, Or Washington ")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\n In which of the months you want to explore? is it (all, january, february, ... , june)\n")
        month = month.lower()
        if month not in ('all','january','february','march','april','may','june','july','august','september','october','november','december'):
            print("Try to enter the month again, it wasn't a valid month!")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: 
        day = input("\n What about the day you are looking for? is it (all, monday, tuesday, ... sunday)?\n")
        day = day.lower()
        if day not in ('sunday','monday','all','tuesday','wednesday','thursday','friday','saturday'):
            print("You entered a not valid day, try again")
            continue
        else:
            break

    print('-'*40)
    return city, month, day

# in this method load the dataset based on which city the user inputs 
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
    # read the csv file using read_csv pandas based on the user input of cit
    # I have decided to add the option all because why not exploring all of them together giving a broader view 
    if city not in ('all'):
        df = pd.read_csv(CITY_DATA[city])
    else:
        # for all dataframes if the user choses all combine them
        dfs = []
        for city, path in CITY_DATA.items(all):
            dfC = pd.read_csv(path)
            dfs.append(dfC)
        
        df = pd.concat(dfs, ignore_index=True)
    ## print(df)
    return df

## this metohd I created to clean the data 
## cleaning the data included handling missing data 
# also handle the high cardinality of dates
def clean_data(df):
    df = handle_dates(df)
    df = handle_missing(df)
    return df

# this method I created to handle the missing data
def handle_missing(df):
    # I chose to fill them with Unknown 
    print('We have {} missing enteries'.format(df.isnull().sum().sum()) )
    # fill Nan values using fillna method
    df.fillna('Unknown', inplace=True)
    print('These were filled by (Unknown) ')
    return df

## this method I created to handle teh dates
def handle_dates(df):
    """
    Handle the dates as their datatypes using to_datetime pandas
    """
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Birth Year'] = pd.to_datetime(df['Birth Year'])

    ## this coulmn has high cardinality so I better create new coulmns that I can filter by
    # Like the day of the week and the month and the year and the time
    df['start_month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['start_day'] = df['Start Time'].dt.strftime('%A').str.lower()
    df['start_year'] = df['Start Time'].dt.strftime('%Y')
    df['start_time'] = df['Start Time'].dt.strftime('%X')
    
    df['end_month'] = df['End Time'].dt.strftime('%B').str.lower()
    df['end_day'] = df['End Time'].dt.strftime('%A').str.lower()
    df['end_year'] = df['End Time'].dt.strftime('%Y')
    df['end_time'] = df['End Time'].dt.strftime('%X')
    
    # we have also the coulmn of Birth year 
    # df['Birth Year'] = pd.to_datetime(df['Birth Year'], format='%Y')
    # this is not working for users stats 
    # I have decided to handle this one as integer to get the min and max values
    df['Birth Year'] = pd.to_numeric(df['Birth Year'],errors='coerce' , downcast='integer')

    # dropped them after I handeld them
    df.drop('Start Time', axis=1, inplace=True) 
    df.drop('End Time', axis=1, inplace=True) 

    return df

# this method get the time travel frequent times
# to get that I used the mode built-in method
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month
    print('The most frequent month is: ', df['start_month'].mode()[0])
    
    # the most common day of week
    print('The most frequent day is: ', df['start_day'].mode()[0])

    # the most common start hour
    print('The most commoon start hour is: ', df['start_time'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# in this method I get some statics about the stations of the trip
# used mode and groupby 
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    print('The most commonly used start station is: ', df['Start Station'].mode()[0] )

    # most commonly used end station
    print('The most commonly used end station is: ', df['End Station'].mode()[0] )

    # most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is: ', 
          df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# In this method I get some statics about the trip duration 
# used the sum, mean aggregation functions
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    # the trip duration coulmn is in seconds 
    # to make it more readable I convert it to days by dividing it on 86400
    print('The total travel time in hours is: ', df['Trip Duration'].sum()/86400)

    # mean travel time
    print('The average travel time in minutes is: ', df['Trip Duration'].mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# In this method I get some statics about the users
# Using 
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    print('In this city, we have diffrent types of users as follows: ')
    print(df['User Type'].value_counts())

    # counts users based on gender
    print('The total count of each gender is as follow: ')
    print('Females:', df['Gender'].value_counts().get("Female", 0))
    print('Males:', df['Gender'].value_counts().get("Male", 0))
    print('Unknown:', df['Gender'].value_counts().get("Unknown", 0))

    # So because I don't want to include the unknown value of these I will use a filter on the dataset 
    #  earliest year of birth 
    print('The earliest year of birth is: ', df['Birth Year'].min())

    # Something doesn't add up here because it first displays to me the (unknown) so because I used it to fill the missing data
    # I am thinking to impute the missing birth year with the mode of it 
    # but this will effect the time since I already imputed why impute twice
    # so what can I do ?

    #  most recent of birth 
    print('The most recent year of birth is: ', df['Birth Year'].max())

    #  most common year of birth
    print('The most common year of birth is: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    # start the program until the user hits no
    while True:
        # gets the filters 
        city, month, day = get_filters()

        # load the dataset
        df = load_data(city, month, day)

        # clean the dataset
        df= clean_data(df)

        # Display diffrent statics of the dataset
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

############################

# In this project the dataset of diffrent city is explored
# by the user interactivly of diffrent cities

############################
if __name__ == "__main__":
	main()