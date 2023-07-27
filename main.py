from sqlite3 import OperationalError, IntegrityError, ProgrammingError
from controller import controller as c
from model import Event_Table
from pdf_scraper import PDF_Scraper as scr

if __name__ == '__main__':
    competition_name = "AbC"
    
    m = Event_Table()

    pdf1 = "073.pdf"
    pdf2 = "Crystal Reports ActiveX Designer - 2023Vail_013Preliminary_FS_StartingOrderWithClubNames.pdf"

    contents = scr.stage_pdf(pdf1)
    event_dict = scr.handle_6_0(contents)

    

