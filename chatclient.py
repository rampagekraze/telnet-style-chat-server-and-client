import curses
import select, socket, sys
import time

BUFSZ=512
srvaddr = ('192.168.17.*', 1776)
sock = None

#log = file('chatlog', 'w')

def chatter(_):
    display = curses.newwin(curses.LINES-2, curses.COLS, 0, 0)
    display.scrollok(1)
    status = curses.newwin(1, curses.COLS, curses.LINES-2, 0)
    echo = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
    echo.keypad(1)

    st = "MESSAGE"
    st+=' '*(curses.COLS-len(st)-1)
    status.addstr(st, curses.A_REVERSE)
    status.noutrefresh()
    buf = ''
    start=time.time()
    while True:                
        curses.doupdate()
        rfds,_,_ = select.select([sock,sys.stdin],[],[])
 #       log.write("%s: rfds: %s\n" % (time.time()-start, rfds)) 
 #       log.flush()
        if sock in rfds:
            y,x = display.getyx()
            display.addstr(sock.recv(BUFSZ)+'\n')
            if y > curses.LINES-3:
                display.scroll(1)
            display.noutrefresh()
        if sys.stdin in rfds:
            ch = echo.getch() 
            if ch == ord('\n'):
            	if buf.startswith('/ban'):
            		raw_input('\n\n\nwho:')
            	buf = ''
                if buf.startswith('/q'):
                    sys.exit(0)
                sock.send(buf)
                buf = ''
            elif ch == 8 or ch == 127:
                buf = buf[:-1]
            elif ch <= 256:
                buf+=chr(ch)

        echo.clear()
        echo.move(0,0)
        echo.addstr(buf)
        echo.noutrefresh()
        

stdscr = curses.initscr()
stdscr.timeout(1)   
curses.noecho()
curses.cbreak()
curses.curs_set(0)

sock = socket.socket()
sock.connect(srvaddr)

curses.wrapper(chatter)

sock.close()

curses.curs_set(1)
curses.nocbreak()
curses.echo()

curses.endwin()
