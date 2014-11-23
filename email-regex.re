(?=postmaster@|POSTMASTER@|mailer-daemon@|MAILER-DAEMON@[.\n\t\s]X-Failed-Recipients:|\bfailure\b[.\n])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}) # Attempt at finding invalid email

(From\s).*@xxx # For finding number of emails in mbox file

From:.+(postmaster@|POSTMASTER@|mailer-daemon@|MAILER-DAEMON@) # First indicator of email containing an invalid email
Subject.+(mail\sdelivery\sfailure)
Subject.+(returned\smail:\ssee\stranscript\sfor\sdetails)

(?<=X-Failed-Recipients:\s)([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}) # For finding invalid emails from gmail's servers