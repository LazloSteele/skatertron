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
        
        text = extract_text(pdf)

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
        except:
            raise ValueError('No valid skaters found!')


        event = {
            'num': event_number,
            'name': event_name,
            'skaters': skaters
            }

        return(event)

    @staticmethod
    def skaters_ijs(pdf):
        content = extract_text(pdf)
        print(content)
        match = re.findall(r'(\d+\n)+', content)

        print(match)
        
        '''
        removes extreneous data that is inconsistent in the data ordering in the pdf sources
        '''  
        #to_remove = ['Starting', 'Number', 'Name', 'Nation']
        #for n in to_remove:
        #    contents.remove(n)

        '''
        number_of_skaters = 0
        for n in contents:
            try:
                int(n)
                number_of_skaters += 1
            except:
                pass

        #wtf is this string indexing for? Clean this up.    
        skaters = [n for n in contents[(3+number_of_skaters):-3]]
        skaters = skaters[::2]
        '''
        pass

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
    event = PDF_Scraper.stage_pdf(pdf, '6.0')

    print(event)


