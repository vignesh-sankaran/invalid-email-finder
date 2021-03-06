# Design documentation

This document's purpose is to highlight and discuss design decisions that were made in the creation of
this script for Engineers Without Borders Australia (EWB), so that any individual that either works on
the project within EWB or forks the project, will understand the logic behind the decisions that were
made in the creation of this script. Due to the fact that this script was mostly hacked together within
a week, it may have a low success rate in finding invalid emails. Nonetheless, it is necessary to
explain design decisions when they are made. 

## Overview
The purpose of this script is to capture and record invalid emails that are contained within a mbox
file. These files are the backup files of an email address' inbox, so they can be quite large.
Consequently, going through a .mbox file will take a considerable amount of time, perhaps upwards
of 10 seconds on a file with > 2.5 million lines of text. 

The script relies upon a certain number of assumptions to be true of potentially invalid emails in
order to extract them out, which is discussed in detail below. 

## Technical choices

### Language
Python was chosen because of its easy to read syntax, assisting in the understanding of this script
for any following people working on this script, whether at EWB or on GitHub. 

### Initial tasks prior to invalid email finding:
One must supply a valid directory to the .mbox file in question. For reasons unknown, the OS package
in python doesn't accept inserted directories with "~/" in them. So one must supply the full,
non abbreviated directory to the file in question. 

Another usability problem at this point is the inability to quit the script when being prompted to
enter a valid directory. This is something to consider fixing in the next version of this script.

After one supplies the directory, it is a simple matter of validating the directory via the OS package
(and asking the user to re insert a directory if it is invalid), checking to see that the directory
supplied points to a .mbox file, and importing the mbox file into the script via the mailbox package. 

### Handling the mailbox and emails within
Python comes with the mailbox package by default. This package allows one to import a .mbox file as
an object, and consists of emails that are also their own object. which means that rather than having
to search the entire .mbox file manually with a regular expression, it is now possible to navigate
each email individually and access the email's fields directly e.g. FROM. 

### Heuristic
Emails that bounce from email servers are delivered in a format called Delivery Status Notifications
(DSNs). Unfortunately, email providers, whether private corporations, universities, or email providers
e.g. Gmail, use their own, slightly different format for sending these messages, making it impossible
to use just one method of finding an invalid email. After much researching, the following methodology
was used to find DSN's and within them, the invalid email address the message states the failure for. 

The first check used to find an invalid email address was to ensure that the word "delay" is not in
the subject line. Delayed emails are excluded from the search because although they mostly result
in a failure to send, whether they eventually send to a valid email address is not always possible
to determine. Thus, delayed emails are excluded. 

The next check is again the subject line, to check if the key words "undeliverable", "fail",
"undelivered mail", or "returned mail" appear. These words were chosen based on an analysis for
potential DSNs in an .mbox file given by EWB. These words far from cover all of the possible words
used in a DSN, and there will probably be some DSNs that miss this test. 

After checking the subject line, the next check is to find a FROM email address that begins with
postmaster@ or mailer-daemon@. Based on some prior analysis of an .mbox file provided by EWB, these
two addresses were indicative of a DSN. Unfortunately, any DSNs that are not from the above email
addresses will not be detected, and it is unknown what other email addresses they could come from. 

If the email address is from mailer-daemon@googlemail.com, the email is from Gmail. Gmail DSNs
come with a field known as X-Failed-Recipients. This makes picking up invalid emails bounced from
Gmail very simple and a non issue :).

### DSNs from multipart emails 
The next possibility is if the mailer-daemon@ sourced email is recognised as multipart by the
mailbox package. Multipart emails can have their respective parts accessed using array notation
e.g. email.get_payload(1). As a matter of note, extracting a subpart of a multipart email requires
the syntax email.get_payload(1).get_payload(), since doing email.get_payload(1) will only return
the memory address of the email subpart. 

One of the parts of the email has a part that looks like this:

```
From nobody Wed Nov 26 20:29:41 2014
Final-Recipient: rfc822;test@test.com
Action: failed
Status: 5.0.0 (permanent failure)
Diagnostic-Code: smtp; 5.1.1 - Bad destination email address 'reject' (delivery
 attempts: 0)
```

Multipart emails from both postmaster@ and mailer-daemon@ email addresses have this part at the same
array index (1 for this particular file that was used), but there may be emails that don't have it
at this particular index. In an attempt to manage this potential problem, a mailbox package function,
msg.walk() (more here: https://docs.python.org/2/library/email.message.html?highlight=walk#email.message.Message.walk)
is used to go through each part and eventually find the part that has the Final-Recipient field in it.
By default, if a field is not found, a None object type unique to Python is returned.  

The key field here are Final-Recipient. In a future update, a test for Action to ensure that it states
"failed" rather than another error message that may have been missed in the test of the subject line
will also be included.

As visible in the above example, the Final-Recipient field has a rfc822; preceding the email address
that is to be extracted. Some had capital RFC, some had a space trailing the semicolon before the
email. To extract the email, the regular expression ``(?<=rfc822;)(.)+`` was used. 

### Regex explanation
Regular expressions may appear complicated, but are actually relatively simple in their operation
and their meaning. 
() is a group. 

?<= is a positive lookbehind. Positive in this instance means that we want this condition to be met.
A lookbehind is a statement that means that when the regular expression engine reaches a point in text,
the text string "rfc822;" must be behind the point in order to capture the next group. Lookbehind
statements are known as non-capturing groups. That is, a true lookbehind statement will not return a
value. 

. is a wildcard character that represents any character except a new line. + means pick up 1 or more
of these characters. 

The problem with this regular expression is that the retrieved email sometimes has a trailing space
in front of it. Python has a .strip() method that is used in the script to remove all trailing and
leading white spaces. 

The above test for retrieving an invalid email from is also used for multipart emails deriving from
postmaster@ email addresses. 

#### Non multipart emails
In the provided .mbox file, there were potential non multipart DSNs from postmaster@ email addresses.
There were 2 however, sourced from mailer-daemon@ email addresses. Both of these emails were
specifically from the qmail email server program. To cater for this particular email program, the
key words "Connection refused" and "permanent error" are used to ensure that the DSN is caused by an
invalid email. A regular expression is then used to extract the email address between the angled
brackets. In v0.1, the following regular expression was used for the purpose of extracting the
invalid email address:

```
(?<=[<])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6})
```

Once again, a lookbehind is used to check for the angled bracket `<` prior to the email. `[]` represents
a character class, which is used to search for a specific set of characters definied within the square
brackets. The email address is stored within `<>`. There may be other fields with values between angled
brackets, so it is not possible to use a wildcard `(.)` to search for everything within angled brackets. 

First, the text prior to the @ symbol is picked up. The character class `[A-Za-z0-9._%+-]` is used to
pick up any character that is a capital or lower case letter, all numbers between 0 to 9, and the symbols
`_`, `%`, `+`, and `-`. To ensure that this expression picks up every character prior to the `@` in an
 email, `+` precedes the character class. 

Finding the part of the email address following the @ but before the first full stop is a simple reuse
of the previous character class to find it.

`\.` represents a full stop, the preceding backslash is necessary because a full stop without the
escape backslash is a wildcard representing any character except a newline (i.e. a line break). 

`[A-Za-z]{2,6}` means that up to 2 to 6 letters can be found after the full stop.

The problem with the above regular expression is that it will find an email, but will not recognise
emails with domains longer than 2 parts, or other unique domains. In other words, it will recognise
the email domain @gmail.com, but potentially not @business.melbourne or @student.monash.edu. To
resolve this potential issue, the regular expression was modified to its current form in v0.11:

```
(?<=[<])([A-Za-z0-9._%+-]+@.+)(?=[>]{1})
```

The change made here is that a wildcard is used to pick up the remaining characters after the `@`.
However, this will also pick up the angled bracket > following the email address. To resolve this issue,
a positive lookahead `(?=)` is used to check if 1 angled bracket lies ahead of the end of the email address. 

Unfortunately, another way to retrieve invalid email addresses from other non multipart emails is unknown.
The only way to resolve this is to further consult with experts in the email standards and its
implementation across different email service providers and email server programs.


### Removing duplicates and saving to .csv file:
Extracted emails are stored in a list. The list is then processed to remove duplicates from the list. `set()`
finds the unique elements within a list. list() ensures that the output is in a list.

Python's csv package method `.write()` expects a multidimensional list. However, the email list is a single
dimension list. To work around this issue, an individual row is written for the heading, and an individual
row is written for each email manually via a foreach loop. 