import sqlite3
import re
import os
from pdfminer.high_level import extract_pages, extract_text

class event_table():
    def __init__(self):
        self.events = []
        self.cwd = os.getcwd()
        self.server = None
        self.cursor = None

    def stage_pdf(self

    def handle_pdf(self, pdf, level):
        text = extract_text(pdf)
        event_name = ''
        skaters = []

        contents = list(filter(lambda x: x != '', text.split("\n")))

        if level == "IJS":     
            to_remove = ["Starting", "Number", "Name", "Nation"]
            for n in to_remove:
                contents.remove(n)

            event_name = contents[2].rstrip().upper()
            
            number_of_skaters = 0
            for n in contents:
                try:
                    int(n)
                    number_of_skaters += 1
                except:
                    pass
            
            skaters = [n for n in contents[(3+number_of_skaters):-3]]
            skaters = skaters[::2]

        if level == "6.0":
            event_name = contents[1].rstrip().upper()

            for i in contents:
                pattern = re.compile(r"^[0-9]+\.\s(.*),")
                match = pattern.findall(i)
                if match:
                    this_skater = match[0]
                    skaters.append(this_skater)


        for skate in skaters:
            self.cursor.execute("INSERT INTO skates VALUES(?,?,?)", (event_name, skate, None))
        print(f"inserted {event_name} into table")

    def set_server(self, connection_name):
        self.server = sqlite3.connect(f"{connection_name}.db")
        self.cursor = self.server.cursor()

        try:
            self.cursor.execute("CREATE TABLE skates(event_name, skater, file)")
            self.cursor.execute("CREATE TABLE orders(order_id, email, item)")
        except:
            pass

    def get_skates_all(self):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates")

        for skate in skates:
            print(skate)

    def get_skates_by_evt(self, evt):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates WHERE event_name = (?)", (evt,))

        for skate in skates:
            print(skate)

    def get_skates_by_skater(self, skater):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates WHERE skater = (?)", (skater,))

        for skate in skates:
            print(skate)

    def process_files(self):
        skates = self.cursor.execute("SELECT * FROM skates WHERE file IS NOT NULL")

        for skate in skates.fetchall():
            print("in the second for loop")
            evt = skate[0]
            sk8r = skate[1]
            fn = f"{sk8r} - {evt[6:]}.txt"
            path = f"{evt}/{fn}"
            
            try:
                os.mkdir(evt)
                print("making directory")
            except FileExistsError:
                print("directory exists")
            
            os.rename(skate[2],path)
            print("renamed")
            self.assign_file(evt,sk8r,path)
            
        self.server.commit()
        print("server updated")


    def assign_file(self, evt, skater, file):
        self.cursor.execute(f"UPDATE skates SET file = (?) WHERE event_name = (?) AND skater = (?)", (file, evt, skater))

    def delete(self):
        self.cursor.execute("DELETE FROM skates")

    def export_events(self):
        self.server.commit()
