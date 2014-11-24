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
	subject_not_undeliverable_fail = 0 # Variable that counts for all other subject headings from potentially bounced emails that 
	message_body_list = [] # List variable to storing the messages that meet the valid criteria
	subject_list = [] # List variable for getting subject lines from emails meeting criteria

	# A single for loop was used to iterate through the mbox file for performance reasons
	print "Looping through emails. Please wait..."
	for message in inbox:
		total_emails += 1
		message_subject = message.get('Subject', '').lower()
		message_from = message['from'].lower()
		if DELAY not in message_subject:
			if POSTMASTER in message_from or MAILER_DAEMON in message_from:
				potential_bounced_email_count += 1
				if FAIL in message_subject or UNDELIVERABLE in message_subject or UNDELIVERED_MAIL in message_subject or RETURNED_MAIL in message_subject:
					message_body_list.append(message.get_payload());
					subject_list.append(message_subject) #extend() seems to only add the first character of the subject to the subject list

	# Write email messages that meet the above criteria to a text file
	print "Writing emails to a text file..."
	emails = open('emails.txt', 'a')
	for index in range(len(message_body_list)):
		emails.write(str(message_body_list[index]))
	emails.close()
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