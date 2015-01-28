import time
def follow(thefile, target):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         target.send(line)

def grep(pattern,target):
    while True:
         line = (yield)
         if pattern in line:
             target.send(line)

def printer():
    while True:
        line = (yield)
        print line,

if __name__ == '__main__':
    f = open("access-log")
    co_printer = printer()
    # start it
    co_printer.next()

    # chain it
    co_grep = grep('python', co_printer)
    co_grep.next()

    follow(f, co_grep)
