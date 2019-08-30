**AppFunc**


This app include these functions:
1.	increment()
Adds a search to a collection. The search term should be assigned randomly from the attached list of search terms.
2.	num_last_minute()
Queries the collection to return the number of searches made in the past minute (Hint: this can be done in O(log(n))).
3.	num_arbitrary_lookback(seconds)
Given a number of seconds returns the number of searches made in that time interval (should be an abstraction of Q2).
4.	most_common_term(seconds)
Given an arbitrary lookback, find the most commonly searched term.

Global variables in app_funcs.py are:

PATH = 'c:\IKI\_test_conductor'
STORAGE_FILE_NAME = 'data_storage.json'
TERMS_FILE_NAME = 'phrases_ns.csv'

You can change them according to your preferences.

Before run functions 2-4, you should run func 1 to generate data storage  data from which will be used for further calculation.
You can run the app from command line, just initialize the path to the project location and activate evn conductor_test. 
Requirements are in requirements.txt. 
Then you can call all of the functions from app_funcs.py.


The data structure is list of dictionaries and stored in JSON format in the project folder.
If searches are frequent, I consider to collect load them to json, it can tke time.
Probably is better to collect them to list for some time and then add it to JSON.
Basically, generators are better choice in this case.

