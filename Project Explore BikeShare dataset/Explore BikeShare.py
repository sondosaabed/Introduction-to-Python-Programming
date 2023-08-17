#####
##### Sondos Aabed Explores the Bikeshare Dataset
#####

### Importing the necessary libraries
import time
import traceback # I used this to trace back the error catched
import pandas as pd
# import numpy as np I didnit actually use np

#### this is the csv files dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

## in this method i take the user input and handle the entries to make sure they are valid
def entery_validation(input_message, valid_inputs, invalid_messgae):
    """
    Function that verifies the user input and if there was a problem it returns a prompt
    Args:
        (str) input_message - the message displayed to ask the user of input
        (list) valid_inputs - a list of enteries that are valid
        (str) invalid_messgae - a message to be displayed if the input is invalid
    Returns:
        (str) input - returns the input when it's valid
    """
    ## while 
    while True:
        input_value = str(input("\n"+ input_message +"\n"))
        input_value = input_value.lower()
        if input_value not in valid_inputs:
            print(invalid_messgae)
            continue
        else:
            break
    return input_value

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
    # because this is a redundunt code It was suggested to create anpther method that takes a message and returns the input if valid
    ####
    
    """ City input """
    city_input_message = "Which City would like to explore? All, Chicago, New york city, Or Washington?"
    city_invalid_message = "Try to enter another city that is either: Chicago, New york city, Or Washington "
    city_valid_enteries = ('all','new york city', 'chicago', 'washington')
    # get user input for city (chicago, new york city, washington). 
    city = entery_validation(city_input_message, city_valid_enteries,city_invalid_message)

    """ Month input """
    month_input_message = "In which of the months you want to explore? is it (all, january, february, ... , june)"
    month_invalid_message = "Try to enter the month again, it wasn't a valid month!"
    month_valid_enteries = ('all','january','february','march','april','may','june','july','august','september','october','november','december')
    # get user input for month (all, january, february, ... , june)
    month = entery_validation(month_input_message, month_valid_enteries, month_invalid_message)

    """ Day input """
    day_input_messgae = "What about the day you are looking for? is it (all, monday, tuesday, ... sunday)?"
    day_inavlid_message = "You entered a not valid day, try again"
    day_valid_enteries = ('sunday','monday','all','tuesday','wednesday','thursday','friday','saturday')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = entery_validation(day_input_messgae, day_valid_enteries, day_inavlid_message)

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
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        # for all dataframes if the user choses all concate them
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
def clean_data(df, city):
    """
    Args:
        (pandas dataframe) df - takes a data frame with missing data probabloy and with not proper datatypes probably
        (city) df - because in the case of washington some coulmns doesn't exists
    Returns:
        (pandas dataframe) df - imputed with unknown and date handled
    """
    df = handle_dates(df, city)
    df = handle_missing(df)
    return df

# this method I created to handle the missing data
def handle_missing(df):
    # when I have created the method display data I have notived that there
    # is a missing coulmn name so I searched for it stands for on kaggle
    # and it makes since that this is the bike ID, I think in this case
    # the bike ID is irrelvant so I made the decision to drop it 
    # althought a possible query comes to mind what if there is a frequent bike ID for example
    # in this project scope it is decided to drop it then
    # print(df.columns) it is at index 0
    df.drop(df.columns[0], axis = 1, inplace=True)

    # I chose to fill them with Unknown 
    print('We have {} missing enteries'.format(df.isnull().sum().sum()) )
    # fill Nan values using fillna method
    df.fillna('Unknown', inplace=True)
    print('These were filled by (Unknown) ')
    return df

## this method I created to handle teh dates
def handle_dates(df, city):
    """
    Handle the dates as their datatypes using to_datetime pandas
    """
    # convert to the proper data type 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

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
    
    if city in ('new york city', 'chicago'):
        df['Birth Year'] = pd.to_datetime(df['Birth Year'])
        # we have also the coulmn of Birth year 
        # df['Birth Year'] = pd.to_datetime(df['Birth Year'], format='%Y')
        # this is not working for users stats 
        # I have decided to handle this one as integer to get the min and max values
        df['Birth Year'] = pd.to_numeric(df['Birth Year'],errors='coerce' , downcast='integer')

    # dropped them after I handeld them
    df.drop('Start Time', axis=1, inplace=True) 
    df.drop('End Time', axis=1, inplace=True) 

    return df

# In this function I ask the user if they want to see 5 of the rows
# I use the head method build in by pandas to do that
def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_locaction = 0

    # I actually will famalrize myself with df.iloc, I like the suggestion, the idea that I went for here that also came to my mind is 
    # using the head function with its parameter 
    
    while view_data == 'yes':
        # while the usr wish to print print
        # print(df.head(start_locaction))

        # So I started this solution but It doesn't actually perform this functionality 
        # it prints from the first 
        # So I will go for the suggested way hhhhhh
        
        #using iloc
        print(df.iloc[start_locaction:start_locaction+5])
        # change the start location of the head print
        start_locaction=start_locaction +5
        view_data = input("Do you want to proceed showing the next 5 rows?\n").lower()

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
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    print('In this city, we have diffrent types of users as follows: ')
    print(df['User Type'].value_counts())

    # this condition because the washington csv doens't include gender and year birth coulmns
    if city in ('new york city', 'chicago'):
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
    # start the program until the user hits no ot there exists an exception
    try:
        while True:
            # gets the filters 
            city, month, day = get_filters()

            # load the dataset
            df = load_data(city, month, day)

            # clean the dataset
            # Here I pass the city because in case the city is washington 
            # coulmns Gender and Birth Year coulmns doesn't exist 
            df= clean_data(df, city)

            # ask the user if they want to print the data
            display_data(df)

            # Display diffrent statics of the dataset
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            # Here I pass the city because in case the city is washington 
            # coulmns Gender and Birth Year coulmns doesn't exist 
            user_stats(df, city)

            # the user can restart and try diffrent cities if they 
            # key hit no the program will hault 
            restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
            if restart.lower() != 'yes':
                break
    # Any exception that occures will be printed and traced 
    except Exception as e:
        print("The program encountered an error: ", 
            type(e).__name__, " : ", e)
        traceback.print_exc()

############################

# In this project the dataset of diffrent city is explored
# by the user interactivly of diffrent cities

############################
if __name__ == "__main__":
	main()
