import time
def follow(thefile):
  thefile.seek(0,2) # Go to the end of the file
  while True:
    line = thefile.readline()
    if not line:
      time.sleep(0.1) # Sleep briefly
      continue
    yield line

def grep(pattern,gen_lines):
  for line in gen_lines:
    if pattern in line:
      yield line

logfile = open("access-log")
loglines = follow(logfile)
pylines = grep("python",loglines)

for l in pylines:
    print l
