#!/usr/bin/python3

import gzip
import re
import os
import time
from datetime import date

# location of the MEDLINE 2018 files (baseline and updates)
source_directories = ("/pstore/data/i2e/i2e_sources/Source_Data/MEDLINE_download/2018/Base/",
"/pstore/data/i2e/i2e_sources/Source_Data/MEDLINE_download/2018/Updates/")

# output file for all emails and first time they appear
output_file = "medline_email_first_time.txt"

f_out = open(output_file, "w")

months = {"jan" : 1, "feb": 2, "mar" : 3, "apr" : 4, "may" : 5, "jun" : 6, "jul" : 7, "aug" : 8, "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}
seasons = {"spring" : 3, "summer" : 6, "fall" : 9, "autumn" : 9, "winter" : 12}
email_count = 0
email = ""
pmid = "0"
month = "1"
day = "1"
email_list = {}
email_first_time = {}
pmid_first_time = {}
pubdate_area = 0

# list input MEDLINE files
input_files = []
for source_directory in source_directories:
    files = os.listdir(source_directory)
    for file in files:
        input_file = os.path.join(source_directory, file)
        input_files.append(input_file)

# read each MEDLINE file
file_counter = 0
for input_file in input_files:
    if re.search("\.gz", input_file):
        file_counter+=1
        print("File #" + str(file_counter) + " being processed: "+ input_file)
        f = gzip.open(input_file, "rb")
        # for each file read every line
        for line in f:
            line = line.decode("utf-8")
            # end of MEDLINE record detected
            if re.search("</PubmedArticle",line):
                pmid = "0"
                month = "1"
                day = "1"
                year = "1"
            # read information related to publication date
            # and translate into year, month and day
            if re.search("<PubDate",line):
                pubdate_area = 1
            if re.search("</PubDate",line):
                pubdate_area = 0
            if pubdate_area == 1:
                if re.search("<Year>(.+)<\/Year>",line):
                    matched = re.search("<Year>(.+)<\/Year>",line)
                    year = matched.group(1)
                if re.search("<Month>(.+)<\/Month>",line):
                    matched = re.search("<Month>(.+)<\/Month>",line)
                    month = matched.group(1)
                    if month.lower() in months.keys():
                        month = months[month.lower()]
                if re.search("<Day>(.+)<\/Day>",line):
                    matched = re.search("<Day>(.+)<\/Day>",line)
                    day = matched.group(1)
                if re.search("<MedlineDate>(.+)<\/MedlineDate>",line):
                    matched = re.search("<MedlineDate>(.+)<\/MedlineDate>",line)
                    medline_date = matched.group(1)
                    if re.search("([0-9][0-9][0-9][0-9])", line):
                        matched = re.search("([0-9][0-9][0-9][0-9])", line)
                        year = matched.group(1)
                    if re.search("([0-9]+)\/([0-9]+)\/([0-9]+)", line):
                        matched = re.search("([0-9]+)\/([0-9]+)\/([0-9]+)", line)
                        year = matched.group(3)
                    if re.search("(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", line.lower()):
                        matched = re.search("(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", line.lower())
                        month = matched.group(1)
                    if month.lower() in months.keys():
                        month = months[month.lower()]
                    else:
                        if re.search("(summer|winter|fall|spring|autumn)", line.lower()):
                            matched = re.search("(summer|winter|fall|spring|autumn)", line.lower())
                            season = matched.group(1)
                            if season in seasons:
                                month = seasons[season.lower()]
            # read the PMID of the XML document
            if pmid == "0":
                if re.search("<PMID",line):
                    if re.search("<PMID.*>(.+)<\/PMID>", line):
                        matched = re.search("<PMID.*>(.+)<\/PMID>", line)
                        pmid = matched.group(1)
            # read the Affiliation sections
            if re.search("<Affiliation>",line):
                if re.search("<Affiliation.*>(.+)<\/Affiliation>", line):
                    matched = re.search("<Affiliation.*>(.+)<\/Affiliation>", line)
                    affiliation = matched.group(1)
                    # identify emails within the affiliation information
                    if re.search("([^\t^\"^\:^ ^\,^\[^\]^\(^\)^\.^\<^\>][^\t^\:^\"^ ^\,^\[^\]^\(^\)]*\@[^\[^\]^\:^\"^ ^\,^\(^\)]+\.[^\t^\:^\"^ ^\,^\.^\)^\(^\<^\>]+)", affiliation):
                        matches = re.findall("([^\t^\"^\:^ ^\,^\[^\]^\(^\)^\.^\<^\>][^\t^\:^\"^ ^\,^\[^\]^\(^\)]*\@[^\[^\]^\:^\"^ ^\,^\(^\)]+\.[^\t^\:^\"^ ^\,^\.^\)^\(^\<^\>]+)", affiliation, re.DOTALL)
                        for match in matches:
                            email = match.lower()
                            # check if email has already been seen
                            pub_date = date(int(year), int(month), int(day))
                            if email not in email_list.keys():
                                email_count+=1
                                email_list[email] = 1
                                pmid_first_time[email] = pmid
                                email_first_time[email] = pub_date
                            # if newly found email is older then replace existing
                            else:
                                if email_first_time[email] > pub_date:
                                    email_first_time[email] = pub_date
                                    pmid_first_time[email] = pmid
        print("Unique emails found so far: " + str(email_count))


# write as output all unique emails found and the first time they appear
print("Writing output...")
for email in email_list.keys():
    f_out.write(email + "\t" + pmid_first_time[email] + "\t" + str(email_first_time[email].year) + "\t" + str(email_first_time[email].month) + "\t" + str(email_first_time[email].day) + "\n")
        
    

print("Total unique emails: " + str(email_count))
