(?:(\bpostmaster@\b|\bPOSTMASTER@\b|\bmailer-daemon@\b|\bMAILER-DAEMON@\b))+[\s\t\r\n\v.]*(?:(X-Failed-Recipients:|\b[Ff]ail(ure|ed(\s\bpermanently\b)?))){1}[\s\t\r\n\v.]*

(?<=X-Failed-Recipients:\s)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}