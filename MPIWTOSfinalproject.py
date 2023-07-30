# Imagine your company uses a server that runs a service called ticky, an internal ticketing system. The service logs events to syslog, both when it runs successfully and when it encounters errors.
#
# The service's developers need your help getting some information from those logs so that they can better understand how their software is used and how to improve it. So, for this lab, you'll write some automation scripts that will process the system log and generate reports based on the information extracted from the log files.
#
# What you'll do
# Use regex to parse a log file
#
# Append and modify values in a dictionary
#
# Write to a file in CSV format
#
# Move files to the appropriate directory for use with the CSV->HTML converter


import re
import operator
errors = {}
users = {}
with open("file.txt") as file:
    lines = file.readlines()
for line in lines:
    result =  re.search(r"(INFO:|ERROR:) ([\w ]+) .*\((\w+)\)$", line)
    if result == None:
        continue
    if result.group(1) == "ERROR:":
        if result.group(2) not in errors:
            errors[result.group(2)] = 1
        else:
            errors[result.group(2)] += 1
        if result.group(3) not in users:
            users[result.group(3)] = {"ERROR": 1, "INFO": 0}
        else:
            users[result.group(3)]["ERROR"] += 1
    if result.group(1) == "INFO:":
        if result.group(3) not in users:
            users[result.group(3)] = {"ERROR": 0, "INFO": 1}
        else:
            users[result.group(3)]["INFO"] += 1
print(errors)
print(users)
errors = sorted(errors.items(), key = operator.itemgetter(1), reverse=True)
users = sorted(users.items())
new_errors = {"Error": "Count"}
new_errors.update(errors)
new_users = {"Username": {}}
new_users["Username"] = {"INFO": "INFO", "ERROR": "ERROR"}
new_users.update(users)
print(new_errors)
print(new_users)
with open("error_message.csv", "w") as file:
    for key, value in new_errors.items():
        file.write(key + "," + str(value) + "\n")
with open("user_statistics.csv", "w") as file:
    for key, value in new_users.items():
        file.write(key + "," + str(value["INFO"]) + "," + str(value["ERROR"]) + "\n")