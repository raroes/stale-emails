#!/usr/bin/python3

# this script estimates the number of stale email addresses in MEDLINE
# based on empirical data modeliled using a linearly time-dependent Bernouilli process

import math
import time
from datetime import date

# data file created by the script count_medline_emails.py
input_file = "medline_email_first_time.txt"

# reference time in which the data was gathered
reference_time = 2018.87
# estimation of staling probability based on the Bernoulli process
def staling_function(x):
    # the value 0.021 was computed in the Bernoulli model estimation notebook within the repository
    output = 0.021*(reference_time - x)
    return output

# open data file
f_in = open(input_file, "r")

# read every line in the data file
# computer the staling probability for each email in each line of the data file
sum_probability = 0
email_count = 0
for line in f_in:
    data = line[:-1].split()
    if len(data) == 5:
        year = data[2]
        month = data[3]
        day = data[4]
        pub_date = date(int(year), int(month), int(day))
        date_value = int(year) + (pub_date.timetuple().tm_yday) / 365
        probability = 1 - staling_function(date_value)
        if probability < 0:
            probability = 0
        # cumulative probability
        sum_probability += probability
        email_count += 1

print("Email count: " + str(email_count))
total_stale = email_count - sum_probability
print("Stale emails estimated: " + str(total_stale))
print("Percentage stale: " + str(100*(total_stale / email_count)) + "%")

