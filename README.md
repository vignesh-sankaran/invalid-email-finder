invalid-email-finder
======================

Goes through a .mbox file and returns a .csv file containing a list of all email addresses that fail to send

To run, run invalid-email-finder.py in bash, and enter the directory to a valid .mbox file. The program will then output a .csv file of the invalid emails the script was able to find.

Initial version 0.01a:
- Accepts and verifies directory to a .mbox file, and picks out invalid email addresses from the file based on probable failed Delivery Status Notification emails

KNOWN BUGS:
- Cannot quit the program when accepting input for the .mbox file's directory
- If there are any non multipart emails from a postmaster@ address, the script will not pick them up
- If a DSN (Delivery Status Notification) comes from an email address other than mailer-daemon@ and postmaster@ address, the script will not pick them up
- If a DSN has a different subject line that does not have the words "fail", "undeliverable", "undelivered mail", and "returned mail", the script will not detect it

All in all, a very limited DSN parser, but this is an alpha first release after all :)

Note that the use of this script comes with NO WARRANTY whatsoever, and you use this script at your own risk.