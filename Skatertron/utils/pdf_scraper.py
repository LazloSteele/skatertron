from pdfminer.high_level import extract_text
from tkinter.filedialog import askopenfilename, askdirectory
import re
from enum import Enum


class EventType(Enum):
    IJS = 'IJS'
    SIX_0 = '6.0'
    IJS_NEW = 'IJS New'


class PDFScraper(object):
    valid_event_types = ['IJS', '6.0']
    evt_num_re = re.compile(r'(?<=\n\()[0-9]+[a-zA-Z]?(?=\))|(?<=\n)[0-9]+[a-zA-Z]?(?= - )')
    evt_name_re = re.compile(r'(?<=\)\s)[a-zA-Z0-9( )\\\/\-]+|(?<= - )[a-zA-Z0-9( )\\/\-]+(?=\s|$)')
    evt_skaters_re_6_0 = re.compile(r'(?<=[0-9]\.)\s*(.*)(?=,)')
    evt_skaters_re_ijs = re.compile(
        r'(\d+\n)+(Starting)?(Number)?(Nation)?(Name)?([a-zA-Z0-9\s\(\)\-&]+)(?=printed at:)'
    )
    evt_skaters_re_ijs_new = re.compile(
        r'(?<=\n[\d+]\s)[a-zA-Z]+[a-zA-Z0-9\s\(\)\-&]+'
    )

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

        if event_type not in [event_types.value for event_types in EventType]:
            raise ValueError('Not a valid event type')

        text = extract_text(pdf)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        stripped_text = re.sub(r'^[ \t]+', '', text, flags=re.MULTILINE)

        try:
            print(text)
            print("\n__________________\n")
            print(stripped_text)

            event_number = PDFScraper.evt_num_re.findall(text)[0].strip().upper()
        except:
            raise ValueError('No valid event number found')

        try:
            event_name = PDFScraper.evt_name_re.findall(text)[0].strip().upper()
        except:
            raise ValueError('No valid event name found')

        try:
            if event_type == '6.0':
                skaters = PDFScraper.evt_skaters_re_6_0.findall(text)
            elif event_type == 'IJS':
                skater_text = PDFScraper.evt_skaters_re_ijs.findall(stripped_text)[0][5].strip()

                skaters = skater_text.split('\n')[::2]
            elif event_type == 'IJS New':
                skater_text = PDFScraper.evt_skaters_re_ijs_new.findall(stripped_text)

                skaters = skater_text
            else:
                raise ValueError('Not a valid event type')

            event = {
                'event_number': event_number,
                'event_name': event_name,
                'skaters': skaters
            }

            return event

        except:
            raise ValueError('No valid skaters found!')


if __name__ == "__main__":

    print(PDFScraper.stage_pdf(askopenfilename(), "6.0"))
