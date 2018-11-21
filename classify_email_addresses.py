#!/usr/bin/python3

# estimate the number of unique emails in MEDLINE and the type of email providers

import re
import json

# list of free email providers such as GMail
email_domains_file = "free_email_services.txt"
# list of university email domains
university_domains_file = "world_universities_and_domains.json"

output_file = "count_emails_per_year.txt"
# email address data from count_medline_emails.py
input_file = "medline_email_first_time.txt"

f_out = open(output_file, "w")

# read university email domains from a json file
print("Reading university emails...")
f_in = open(university_domains_file)
data = json.load(f_in)
university_domains = {}
university_counter = 0
university_domain_counter = 0
for university in data:
    domains = university["domains"]
    university_counter+=1
    for domain in domains:
        university_domains[domain] = 1
        university_domain_counter+=1
print("Read " + str(university_domain_counter) + " domains from " + str(university_counter) + " universities")

# read free email provider list
print("Reading free email domains...")
f_in = open(email_domains_file, "r")

domains = []
free_email_counter = 0
for line in f_in:
    line = line[:-1]
    domain = line
    domains.append(domain)
    free_email_counter+=1
print("Read " + str(free_email_counter) + " free email domains")

f_in = open(input_file, "r")

# count all unique MEDLINE email addresses and classify according to domain
print("Reading MEDLINE emails...")
email_year_count = {}
free_email_year_count = {}
university_email_year_count = {} 
line_counter = 0
for line in f_in:
    line = line[:-1]
    line_counter+=1
    if line_counter / 100 == int(line_counter / 100):
        print(str(line_counter) + " lines read.")
    data = line.split("\t")
    email = data[0]
    free_email = 0
    university_email = 0
    # parse the domain from an email address
    if re.search("@([^\+]+)", email):
        matches = re.search("@([^\+]+)", email)
        domain = matches.group(1)
        # check if domain belongs to a free provider
        if domain in domains:
            free_email = 1
        # check if domain belongs to a university domain
        for university_domain in university_domains.keys():
            if re.search(domain, university_domain):
                university_email = 1
    # count for each type of email
    year = data[2]
    if year in email_year_count.keys():
        email_year_count[year]+=1
        if free_email == 1:
            free_email_year_count[year]+=1
        if university_email == 1:
            university_email_year_count[year]+=1
    else:
        email_year_count[year]=1
        free_email_year_count[year] = 0
        university_email_year_count[year] = 0
        if free_email == 1:
            free_email_year_count[year]=1
        if university_email == 1:
            university_email_year_count[year] = 1

# print table of results
years = sorted(email_year_count.keys())
print("Year\tTotal count\tTotal free\tPercentage free\tTotal university\tPercentage university")
f_out.write("Year\tTotal count\tTotal free\tPercentage free\tTotal university\tPercentage university\n")
for year in years:
    print(year + "\t" + str(email_year_count[year]) + "\t" + str(free_email_year_count[year]) 
          + "\t" + str(free_email_year_count[year]/email_year_count[year])
          + "\t" + str(university_email_year_count[year]) + "\t" + str(university_email_year_count[year]/email_year_count[year]))
    f_out.write(year + "\t" + str(email_year_count[year]) + "\t" + str(free_email_year_count[year])
          + "\t" + str(free_email_year_count[year]/email_year_count[year])
          + "\t" + str(university_email_year_count[year]) + "\t" + str(university_email_year_count[year]/email_year_count[year]) + "\n")
   
