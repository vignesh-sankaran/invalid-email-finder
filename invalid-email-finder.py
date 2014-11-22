#!/usr/bin/env python
import os
import sys
import mailbox
import email

# Global constants
# Constant values for from email addresses. Note that there are no constants in Python
POSTMASTER = "postmaster@"
MAILER_DAEMON = "mailer-daemon@"
DELAY = "delay" # Checking email subjects for the word delay. We don't want to search for emails addresses with delayed sending

# Runs the script
def main():
	print "Welcome to the invalid email finder."
	directory = read_input()
	inbox = import_file(directory)
	find_emails(inbox)

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
	

	# Get unique list of subjects that are from 


	# Constant values for potential message body values pointing to a failed DSN


	# For debugging purposes only
	# test_message_count(inbox)

	postmaster_messages = 0
	criteria_met_count = 0
	
	print "Extracting invalid emails from the mbox file. Please be patient, this could take a while"
	for message in inbox:
		message_from = message['From'].lower()
		# Get the subject of an email, convert to empty string if there isn't a subject
		message_subject = message.get('Subject', '')

		# If subject is not empty, convert it to lower case
		if message_subject != "":
			message_subject = message_subject.lower()

		if POSTMASTER in message_from or MAILER_DAEMON in message_from:
			postmaster_messages += 1
			if DELAY not in message_subject:
				if FAIL in message_subject or UNDELIVERABLE in message_subject:
					criteria_met_count += 1

	print postmaster_messages
	print criteria_met_count

# Find list of subjects that are from emails addresses potentially holding invalid emails (see global constants)
def find_subjects(inbox):
	subject_list = []

# Remove duplicates from a list. In this program, the lists are from the list of subjects from emails and list of invalid email addresses
def remove_list_duplicates(list):
	return

# Tests how many messages are in a mailbox. Only run for debugging
def test_message_count(inbox):
	# For debugging purposes only
	test_count = 0
	for message in inbox:
		test_count += 1
	print test_count
if __name__ == "__main__":
    main()