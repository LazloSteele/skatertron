from pdfminer.high_level import extract_text
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from os import listdir
import re

class PDF_Scraper(object):
    valid_event_types = ['IJS', '6.0']
    evt_num_re = re.compile(r'(?<=\n\()[0-9]+[a-z]?(?=\))')
    evt_name_re = re.compile(r'(?<=\)\s)[a-zA-Z0-9( )\\\/\-]+')
    evt_skaters_re_6_0 = re.compile(r'(?<=[0-9]\.)\s*(.*)(?=,)')
    evt_skaters_re_ijs = re.compile(r'(\d+\n)+([a-zA-Z0-9\s]*)(?=printed at:)')
    
    @staticmethod
    def get_file_path():
        path = askopenfilename()

        return path

    @staticmethod
    def get_dir_path():
        path = askdirectory()

        return path
    
    @staticmethod
    def stage_pdf(pdf, event_type):

        if event_type not in PDF_Scraper.valid_event_types:
            raise ValueError('Not a valid event type')
        
        text = extract_text(pdf).replace('\n\n', '\n')

        try:
            event_number = PDF_Scraper.evt_num_re.findall(text)[0].strip().upper()
        except:
            raise ValueError('No valid event number found')
        
        try:
            event_name = PDF_Scraper.evt_name_re.findall(text)[0].strip().upper()
        except:
            raise ValueError('No valid event name found')

        try:
            if event_type == '6.0':
                skaters = PDF_Scraper.evt_skaters_re_6_0.findall(text)
            elif event_type == 'IJS':
                skater_text = PDF_Scraper.evt_skaters_re_ijs.findall(text)[0][1].strip()

                skaters = skater_text.split('\n')[::2]        
        except:
            raise ValueError('No valid skaters found!')


        event = {
            'num': event_number,
            'name': event_name,
            'skaters': skaters
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

    pdf = PDF_Scraper.get_file_path()
    event = PDF_Scraper.stage_pdf(pdf, 'IJS')

    print(event)


