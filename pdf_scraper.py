from pdfminer.high_level import extract_text
from tkinter.filedialog import askopenfilename, askdirectory
from os import listdir
import re


class PDF_Scraper(object):
    @staticmethod
    def get_file_path():
        path = askopenfilename()

        return path

    @staticmethod
    def get_dir_path():
        path = askdirectory()

        return path
    
    @staticmethod
    def stage_pdf(pdf):
        text = extract_text(pdf)
        contents = list(filter(lambda x: x != '', text.split("\n")))

        return contents

    @staticmethod
    def handle_ijs(contents):

        event_number = ''
        event_name = ''
        skaters = []

        to_remove = ["Starting", "Number", "Name", "Nation"]
        for n in to_remove:
            contents.remove(n)

        event_num_and_name = contents[2].rstrip().upper()
        
        match = re.findall(r"\(.*\)", event_num_and_name)
        if match:
            event_number = match[0][1:-1]
            
        
        event_name = event_num_and_name[len(event_number)+3:]
        
        number_of_skaters = 0
        for n in contents:
            try:
                int(n)
                number_of_skaters += 1
            except:
                pass
            
        skaters = [n for n in contents[(3+number_of_skaters):-3]]
        skaters = skaters[::2]

        event = {
            "num": event_number,
            "name": event_name,
            "skaters": skaters
            }

        return(event)

    @staticmethod
    def handle_6_0(contents):
        
        event_number = ''
        event_name = ''
        skaters = []
        
        event_num_and_name = contents[1].rstrip().upper()
        
        match = re.findall(r"\(.*\)", event_num_and_name)
        if match:
            event_number = match[0][1:-1]
            
        event_name = event_num_and_name[len(event_number)+3:]

        for i in contents:
            pattern = re.compile(r"^[0-9]+\.\s(.*),")
            match = pattern.findall(i)
            if match:
                this_skater = match[0]
                skaters.append(this_skater)

        event = {
            "num": event_number,
            "name": event_name,
            "skaters": skaters
            }        

        return(event)

    @staticmethod
    def bulk_stage_pdf(directory):
        files = listdir(directory)

        contents = []

        for file in files:
            path = f'{directory}\\{file}'

            contents.append(PDF_Scraper.stage_pdf(path))

        return contents

if __name__ == '__main__':
    file = PDF_Scraper.get_file_path()
    content = PDF_Scraper.stage_pdf(file)
    event = PDF_Scraper.handle_ijs(content)
    
    
    IJS = PDF_Scraper.get_dir_path()
    
    IJS_Content = PDF_Scraper.bulk_stage_pdf(IJS)
    IJS_Events = []
    for n in IJS_Content:
        IJS_Events.append(PDF_Scraper.handle_ijs(n))

    print(event)
    print(IJS_Events)
