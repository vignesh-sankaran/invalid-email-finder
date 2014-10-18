(?=postmaster@|POSTMASTER@|mailer-daemon@|MAILER-DAEMON@[.\n\t\s]X-Failed-Recipients:|\bfailure\b[.\n])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6})

(?<=X-Failed-Recipients:\s)([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6})