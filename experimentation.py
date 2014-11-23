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
# Constant value for the word delay, we don't want to be searching for these emails
DELAY = "delay"
# Constant values for words in subject that indicate failed emails
UNDELIVERABLE = "undeliverable"
FAIL = "fail"

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
	subject_list = [] # List variable for getting subject lines from emails meeting criteria

	# A single for loop was used to iterate through the mbox file for performance reasons
	for message in inbox:
		total_emails += 1
		message_subject = message.get('Subject', '').lower()
		message_from = message['from'].lower()
		if DELAY not in message_subject:
			if POSTMASTER in message_from or MAILER_DAEMON in message_from:
				potential_bounced_email_count += 1
				if UNDELIVERABLE not in message_subject and FAIL not in message_subject:
					subject_not_undeliverable_fail += 1
					subject_list.append(message_subject) #extend() seems to only add the first character of the subject to the subject list
			
	# Print first subject in list
	print subject_list[0]

	# Remove duplicated subjects
	unique_subjects = list(set(subject_list))

	# Print out report for user to see.
	print "Total number of emails: %i" % total_emails
	print "Number of potentially bounced emails: %i" % potential_bounced_email_count
	print "Number of subject headings without words undeliverable or fail: %i" % subject_not_undeliverable_fail
	print "List of unique subjects: "
	for subject in unique_subjects:
		print subject
if __name__ == "__main__":
    main()