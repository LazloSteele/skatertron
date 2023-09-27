from pdfminer.high_level import extract_text
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from os import listdir
import re

class PDF_Scraper(object):
    valid_event_types = ['IJS', '6.0']
    
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
            raise ValueError(f'Event type must be one of the following: {valid_event_types}')
        
        text = extract_text(pdf)
        contents = list(filter(lambda x: x != '', text.split('\n')))

        #initialize values for event
        event_number = ''
        event_name = ''
        skaters = []

        if event_type == 'IJS':
            
            '''
            removes extreneous data that is inconsistent in the data ordering in the pdf sources
            '''  
            to_remove = ['Starting', 'Number', 'Name', 'Nation']
            for n in to_remove:
                contents.remove(n)
            
            '''
            name and number of event has always been third element in the pdf after stripping, happy to find better way
            '''
            event_num_and_name = contents[2].strip().upper()

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

            
        elif event_type == '6.0':
            
            event_num_and_name = contents[1].strip().upper()

            # in 6.0 pdf some skaters have a newline character between their skating order # and their name
            # how to regex the list of strings that contents is and also catch the instance of extra newline
            # better preprocessing???
            pattern = re.compile(r'(?<=[0-9]\.)\s*(.*)(?=,)')
            pattern2 = re.compile(r'^[0-9]{0,2}\.\s*')

            #gross bad, bad gross, make this cleaner
            n=0
            for i in contents:
                match = pattern.findall(i)
                this_skater = ''
                
                if match:
                    this_skater = match[0].strip()
                elif pattern2.findall(i):
                    this_skater = re.findall(r'(.*)(?=,)', contents[n+1].strip())[0]

                if this_skater:
                    skaters.append(this_skater)
                
                n+=1

        '''
        pulls any instance of digits and an optional alpha within parenthesis
        positive lookahead and lookbehind to not include the parenthesis
        meant to capture the event number
        '''
        event_number = re.findall(r'(?<=\()[0-9]+[a-z]?(?=\))', event_num_and_name)[0]
        event_name = re.findall(r'(?<=\)\s)[a-zA-Z0-9\s\\\/\-]+', event_num_and_name)[0]
        if not event_number:
            raise ValueError('PDF does not contain expected event number format: \'(001) abc\' -OR- \'(001a) abc\'')

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
    data = PDF_Scraper.stage_pdf(PDF_Scraper.get_file_path(), '6.0')
    print(data)

