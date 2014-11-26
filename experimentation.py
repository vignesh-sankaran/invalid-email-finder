#!/usr/bin/env python
# Author: Vignesh
# License: Apache 2.0
# Purpose: This script experiments with a mbox file for specific factors e.g. number of emails, specific subject types etc

import sys
import mailbox
import email
import re
import os

# Constant values for from email addresses. Note that there are no constants in Python
POSTMASTER = "postmaster@"
MAILER_DAEMON = "mailer-daemon@"
# Constant values for checking subject strings
DELAY = "delay" # Checking email subjects for the word delay. We don't want to search for emails addresses with delayed sending
UNDELIVERABLE = "undeliverable"
FAIL = "fail"
UNDELIVERED_MAIL = "undelivered mail"
RETURNED_MAIL = "returned mail"

# Runs the program
def main():
	# Constant for accessing the mailbox file at its current location
	MBOX_DIRECTORY = "/Users/vignesh/Dropbox/00 EWB/Mail filtering/All mail Including Spam and Trash.mbox"

	# Print output to user
	print "Welcome! This script tests certain aspects of a predefined mbox file"
	print "The mbox file is located at %s" % MBOX_DIRECTORY

	# Import mbox file
	inbox = mailbox.mbox(MBOX_DIRECTORY)

	# Variables for for loop
	total_emails = 0 # Counts total number of emails
	potential_bounced_email_count = 0 # Variable for counting number of potentially bounced emails
	subject_not_undeliverable_fail = 0 # Variable that counts for all other subject headings from potentially bounced emails
	subject_list = [] # List variable for getting subject lines from emails meeting criteria
	email_list = []
	gmail_number_multipart = 0
	gmail_number_non_multipart = 0
	number_multipart = 0
	number_not_multipart = 0
	gmail_count = 0
	non_gmail_count = 0
	postmaster_count = 0
	postmaster_number_multipart = 0
	postmaster_number_not_multipart = 0
	count = 0
	# List variables for storing message bodies based on their subject lines
	md_multipart = []
	md_non_multipart = []
	postmaster = []
	# Compile regex pattern to avoid multiple recompilation and increase efficiency
	pattern = re.compile('(?<=rfc822;)(?:\s)?(.)+', re.IGNORECASE)
	# A single for loop was used to iterate through the mbox file for performance reasons
	print "Looping through emails. Please wait..."
	for message in inbox:
		total_emails += 1
		message_subject = message.get('Subject', '').lower()
		message_from = message['from'].lower()
		if DELAY not in message_subject:
			if FAIL in message_subject or UNDELIVERABLE in message_subject or UNDELIVERED_MAIL in message_subject or RETURNED_MAIL in message_subject:
				if POSTMASTER in message_from or MAILER_DAEMON in message_from:
					potential_bounced_email_count += 1

					if "mailer-daemon@googlemail.com" in message_from:
						# No email from google is multipart, that's ok, we can use the X-Failed-Recipients field instead :D
						gmail_count += 1
						email_list.append(message['X-Failed-Recipients'])

					elif MAILER_DAEMON in message_from and "mailer-daemon@googlemail.com" not in message_from:
						non_gmail_count += 1
						if message.is_multipart() and message.get_payload(1).get_content_type() == 'message/delivery-status':
							number_multipart += 1
							# Get email address stored within second subpart within email header.
							# Now need to figure out why I can't just do it like this: 
							# http://stackoverflow.com/questions/5298285/detecting-if-an-email-is-a-delivery-status-notification-and-extract-informatio

							match = pattern.search(message.get_payload(1).get_payload()[1]['Final-Recipient'])
							email_address = match.group(0).strip()
							md_multipart.append(message.get_payload(1))
							email_list.append(email_address)
						else: # These non multipart emails from mailer-daemon are from the qmail email server program
							message_as_string = str(message.get_payload())
							if 'permanent error' in message_as_string and 'Connection refused' in message_as_string:
								match = re.search('(?<=[<])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6})', message_as_string)
								print match.group(0)
								email_list.append(match.group(0))
							md_non_multipart.append(message.get_payload())
							number_not_multipart += 1

					elif POSTMASTER in message_from:
						postmaster_count += 1
						if message.is_multipart() and message.get_payload(1).get_content_type() == 'message/delivery-status':
							postmaster_number_multipart += 1
							match = pattern.search(message.get_payload(1).get_payload()[1]['Final-Recipient'])
							email_address = match.group(0).strip()
							postmaster.append(message.get_payload(1))
							email_list.append(email_address)

						else:
							postmaster_number_not_multipart += 1

	# Save different email kinds to text files
	print "Writing mailer daemon multipart emails to text file..."
	md_multipart_file = open('1_md_multipart.txt', 'wb') #wb overwrites the file if it exists
	for index in range(len(md_multipart)):
		md_multipart_file.write(str(md_multipart[index]))
	print "Done"

	print "Writing mailer daemon non multipart emails to text file..."
	md_non_multipart_file = open('1_md_non_multipart.txt', 'wb')
	for index in range(len(md_non_multipart)):
		md_non_multipart_file.write(str(md_non_multipart[index]))
	print "Done"

	print "Writing postmaster emails to text file..."
	postmaster_file = open('1_postmaster.txt', 'wb')
	for index in range(len(postmaster)):
		postmaster_file.write(str(postmaster[index]))
	print "Done"
	
	# Print out report for user to see.
	print "Total number of emails: %i" % total_emails
	print "Number of potentially bounced emails: %i" % potential_bounced_email_count

	print "Number of emails in email list: %i" % len(email_list)

	print "Total number of gmail messages: %i" % gmail_count

	print "Total number of mailer daemon messages that are not gmail: %i" % non_gmail_count
	print "Number of multipart non gmail messages: %i" % number_multipart
	print "Number of non multipart non gmail messages: %i" % number_not_multipart

	print "Total number of postmaster messages: %i" % postmaster_count
	print "Number of multipart postmaster messages: %i" % postmaster_number_multipart
	print "Number of non multipart postmaster messages: %i" % postmaster_number_not_multipart
	
if __name__ == "__main__":
    main()