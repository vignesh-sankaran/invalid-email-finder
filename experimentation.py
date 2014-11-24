#!/usr/bin/env python
# Author: Vignesh
# License: Apache 2.0
# Purpose: This script experiments with a mbox file for specific factors e.g. number of emails, specific subject types etc

import sys
import mailbox
import email

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
	# List variables for storing message bodies based on their subject lines
	fail_message_list = []
	undeliverable_message_list = []
	undelivered_mail_message_list = []
	returned_mail_message_list = []
	# A single for loop was used to iterate through the mbox file for performance reasons
	print "Looping through emails. Please wait..."
	for message in inbox:
		total_emails += 1
		message_subject = message.get('Subject', '').lower()
		message_from = message['from'].lower()
		if DELAY not in message_subject:
			if POSTMASTER in message_from or MAILER_DAEMON in message_from:
				potential_bounced_email_count += 1
				subject_list.append(message_subject) #extend() seems to only add the first character of the subject to the subject list
				# Store message body in list depending on subject line
				if FAIL in message_subject:
					fail_message_list.append(message.get_payload())
				elif UNDELIVERABLE in message_subject:
					undeliverable_message_list.append(message.get_payload())
				elif UNDELIVERED_MAIL in message_subject:
					undelivered_mail_message_list.append(message.get_payload())
				elif RETURNED_MAIL in message_subject:
					returned_mail_message_list.append(message.get_payload())

	# Write email messages that meet the above criteria to text files
	print "Writing fail subject emails to text file..."
	fail_emails = open('01fail_emails.txt', 'w') # Second option 'w' represents write a new file if one doesn't exist, otherwise, append to an existing one
	for index in range(len(fail_message_list)):
		fail_emails.write(str(fail_message_list[index]))
	fail_emails.close()
	print "Done"

	print "Writing undeliverable subject emails to text file..."
	undeliverable_emails = open('02undeliverable_emails.txt', 'w')
	for index in range(len(undeliverable_message_list)):
		undeliverable_emails.write(str(undeliverable_message_list[index]))
	undeliverable_emails.close()
	print "Done"

	print "Writing undelivered mail subject emails to text file..."
	undelivered_emails = open('03undelivered_emails.txt', 'w')
	for index in range(len(undelivered_mail_message_list)):
		undelivered_emails.write(str(undelivered_mail_message_list[index]))
	undelivered_emails.close()
	print "Done"

	print "Writing returned mail subject emails to text file..."
	returned_emails = open('04returned_emails.txt', 'w')
	for index in range(len(returned_mail_message_list)):
		returned_emails.write(str(returned_mail_message_list[index]))
	returned_emails.close()
	print "Done"

	# Remove duplicated subjects
	unique_subjects = list(set(subject_list))

	# Print out report for user to see.
	print "Total number of emails: %i" % total_emails
	print "Number of potentially bounced emails: %i" % potential_bounced_email_count
	print "List of unique subjects: "
	for subject in unique_subjects:
		print subject
if __name__ == "__main__":
    main()