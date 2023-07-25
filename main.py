from controller import controller as c
from model import event_table


def __main__():
    c.SET_SERVER(m, "Vail")
    m.delete()
    c.NEW_COMP(m)
    m.server.commit()
    m.assign_file("(008) INTERMEDIATE WOMEN SHORT PROGRAM", "Amelia Greer", "DUMP/Photo/13/New Text Document.txt")
    m.assign_file("(010) EXCEL PRELIMINARY PLUS FREE SKATE", "Jiana Weak", "DUMP/Photo/13/New Text Document - Copy.txt")
    m.server.commit()

    m.process_files()

    
if __name__ == '__main__':
    m = event_table()

    __main__()
    
