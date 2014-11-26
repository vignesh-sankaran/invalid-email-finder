#!/usr/bin/env python
import re
import os
import sys
import mailbox
import email
import csv

# Runs the script
def main():
	print "Welcome to the invalid email finder."
	directory = read_input()
	inbox = import_file(directory)
	email_address_list = find_emails(inbox)
	# Save list to CSV file
	export_emails(email_address_list)

# Read a file directory from the user
def read_input():
	exit = False
	while exit == False:
		# raw_input() is used in Python 2.x, Python 3.x uses input() instead
		directory = raw_input("Enter the full path (i.e. no ~/) to the mbox file: ")
		exit = verify_input(directory)
	return directory

# Verify user input to see if it a directory
def verify_input(directory):
	#Check if the directory points to a mbox file
	suffix = ".mbox"

	if not directory.endswith(suffix):
		print "That is not an mbox file."
		return False

	# Check if directory to mbox file is valid
	if os.path.exists(directory):
		return True
	else:
		print "This is not a valid directory to the mbox file"
		return False

# Find and verify file
def import_file(directory):
	try:
		inbox = mailbox.mbox(directory)
	except:
		print "Invalid mbox file"
		sys.exit()
	return inbox

# Find invalid email addresses and return results in an array
def find_emails(inbox):

	# Constant values for from email addresses. Note that there are no constants in Python
	POSTMASTER = "postmaster@"
	MAILER_DAEMON = "mailer-daemon@"
	GMAIL_EMAIL_ADDRESS = "mailer-daemon@googlemail.com"

	# Constant values for checking subject strings. Based on analysis from experimentation.py
	DELAY = "delay" # Checking email subjects for the word delay. We don't want to search for emails addresses with delayed sending
	UNDELIVERABLE = "undeliverable"
	FAIL = "fail"
	UNDELIVERED_MAIL = "undelivered mail"
	RETURNED_MAIL = "returned mail"

	# The following are words used to search for DSN's from the qmail server program
	PERMANENT_ERROR = "permanent error"
	CONNECTION_REFUSED = "Connection refused"

	# Variables required for use with finding emails:
	email_list = []

	# Regular expression pattern 
	pattern = re.compile('(?<=rfc822;)(?:\s)?(.)+', re.IGNORECASE)
	postmaster_multipart_pattern = re.compile('(?<=[<])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6})', re.IGNORECASE)

	print "Extracting invalid emails from the mbox file. Please be patient, this could take a while"
	for message in inbox:
		message_subject = message.get('Subject', '').lower()
		message_from = message['from'].lower()
		if DELAY not in message_subject:
			# Not entirely sure if there are emails coming in from other sources...
			if POSTMASTER in message_from or MAILER_DAEMON in message_from:
				# The below values to find invalid email addresses were selected based on an analysis of the mbox file provided by Engineers Without Borders
				# These values probably don't cover every single possiblilty
				# These are attempted to be dealt with in the conditions following this if statement
				if FAIL in message_subject or UNDELIVERABLE in message_subject or UNDELIVERED_MAIL in message_subject or RETURNED_MAIL in message_subject:
				
					if GMAIL_EMAIL_ADDRESS in message_from: # Assuming gmail email addresses aren't registered by the mail package as multipart emails
						# No email from google is multipart, that's ok, we can use the X-Failed-Recipients field instead :D
						email_list.append(message['X-Failed-Recipients'])

					elif MAILER_DAEMON in message_from and GMAIL_EMAIL_ADDRESS not in message_from:
						if message.is_multipart():
							# Get email address stored within second subpart within email header.
							# This if statement is to ensure the email is a DSN, since not all emails have the type message/delivery-status
							if action_failed(message):
								email_address = get_email_address(message, pattern)
								email_list.append(email_address)

						else: # These non multipart emails from mailer-daemon are from the qmail email server program
							message_as_string = str(message.get_payload())
							if PERMANENT_ERROR in message_as_string and CONNECTION_REFUSED in message_as_string:
								match = postmaster_multipart_pattern.search(message_as_string)
								email_list.append(match.group(0))

					elif POSTMASTER in message_from:
						if message.is_multipart():

							if action_failed(message):
								email_address = get_email_address(message, pattern)
								email_list.append(email_address)

						# Finding postmaster emails that are not multipart hasn't been implemented yet
						# When one comes along, I'll be interested to see how to extract the failed email from it :)
	email_list = remove_duplicates(email_list)
	return email_list

# Test if a message has the status of failed under the action field as a test of a multipart email being a bounced email
def action_failed(message):
	FAILED = "failed"
	for part in message.walk(): # walk() is a method that allows us to go through each subpart of a message
		if part['action'] == FAILED:
			return True
	return False

# Extract email address from a multipart email. Pattern is provided so that it doesn't have to be recompiled each time this function is run
def get_email_address(message, pattern):
	# Using walk() is a more flexible method of finding Final-Recipient in case an email server returns a multipart email which puts this in another part of an email
	# that is not just the second part
	for part in message.walk(): # walk() is a method that allows us to go through each subpart of a message
		if part['Final-Recipient'] is not None:
			match = pattern.search(part['Final-Recipient'])
			return match.group(0).strip()

# Remove duplicates from a list. In this program, the lists are from the 
def remove_duplicates(inputted_list):
	print "Email addresses in list before removing duplicates: %i" %len(inputted_list)
	cleaned_list = list(set(inputted_list))
	print "Email addresses in list after removing duplicates: %i" %len(cleaned_list)
	return cleaned_list

# Writes the list of emails to a .csv file
def export_emails(email_address_list):
	FILENAME = 'ouput.csv'
	output_file = open(FILENAME, 'wb')
	csv_writer = csv.writer(output_file, delimiter = '\n')
	print "Writing output to CSV file. NOTE: ANY EXISTING output.csv WILL BE OVERWRITTEN!"
	csv_writer.writerow(['Email'])
	for index in range(len(email_address_list)):
		csv_writer.writerow([email_address_list[index]])
	output_file.close()
if __name__ == "__main__":
    main()