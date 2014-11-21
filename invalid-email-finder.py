#!/usr/bin/env python
# 
import os
import sys
import mailbox

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

	#Check if directory to mbox file is valid
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
	return inbox

def find_emails(inbox):
	message_count = 0

	for message in inbox:
		message_from = message['From']
		print message_from

	# for message in inbox:
	# 	if "Fail" in message['Subject'] or :
	# 		message_count += 1
	# print (message_count)
if __name__ == "__main__":
    main()