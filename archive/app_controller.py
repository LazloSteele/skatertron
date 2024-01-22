from competition_controller import BaseController, EventController, SkateController, FileController
from view import TUI as View
from pdf_scraper import PDF_Scraper as ps

from os import mkdir, listdir
from os.path import isdir, isfile, join


class CLIController(object):

    def __init__(self, view, test_mode=True):
        self.v = view
        self.app_state = "init"
        self.valid_actions = ['A', 'B', 'D', 'F', 'Q']

        self.v.welcome()

        if test_mode:
            self.app_state = "competition_loaded"

    def prompt_user(self):
        self.v.display_valid_actions(self.app_state)

        action = input().upper()

        if action in self.valid_actions:
            return action


class PDFScraperController(object):
    @staticmethod
    def add_event(event_type, bulk = False):

        if event_type.upper() == 'IJS' or event_type.upper() == 'I':
            event_type = 'IJS'
        elif event_type == '6.0' or event_type == '6':
            event_type = '6.0'

        files = []
        events = []

        if bulk:
            d = ps.get_dir_path()
            files = [join(d, file) for file in listdir(d)]
            
        else:    
            f = ps.get_file_path()
            files.append(f)

        for file in files:
            skater_dict = ps.stage_pdf(file, event_type)

            events.append(skater_dict)

        return events



def __main__(testing=True):
    running = True

    competition = None

    if not testing:
        competition = input('Please enter competition name: ')

    clic = CLIController(View)
    bc = BaseController(competition)
    event_controller = EventController(bc.session)
    skate_controller = SkateController(bc.session)
    file_controller = FileController(bc.session)

    while running:

        action = clic.prompt_user()

        match action:

            case 'B':
                event_type = input('IJS or 6.0: ')
                print(PDFScraperController.add_event(event_type, True))
            case 'A':
                event_type = input('IJS or 6.0: ')
                event_dict = PDFScraperController.add_event(event_type)
                for event in event_dict:
                    print(event)
                    event_num = event["num"]
                    event_name = event["name"]
                    skates = event["skaters"]
                    event_controller.create_event(event_num, event_name)

                    event_id = event_controller.read_event_by_number(event_num).id

                    for skater in skates:
                        print(type(event_id), skater)
                        skate_controller.create_skate(event_id, skater)

            case 'D':
                flag_type = input('[A]ll events | Event by [N]umber | Events by [S]kater: ')
                match flag_type.upper():
                    case 'A':
                        for event in event_controller.read_all_events():
                            print(event)
                    case 'N':
                        event_number = input('What is the event number?: ').zfill(3)

                        print(event_controller.read_event_by_number(event_number))
                    case 'S':
                        skater_name = input('Which Skater?: ')
                        c.display_event_by_skater(skater_name)

            case 'F':
                event_number = input('What is the event number?: ').zfill(3)
                starts_in_event = c.m.read_skaters_in_event(event_number)
                c.display_event_by_number(event_number)

                skater_name = input('Which Skater?: ')

                try:
                    skater_order = int(skater_name)
                    skater_name = starts_in_event[skater_order - 1]

                except:
                    print("Not a valid input")

                print(skater_name)

                if skater_name in starts_in_event:
                    c.add_file(event_number, skater_name)

            case 'U':
                event_number = input('What is the event number?: ').zfill(3)

                starts_in_event = c.m.read_skaters_in_event(event_number)
                c.display_event_by_number(event_number)

                skater_name = input('Which Skater?: ')

                try:
                    skater_order = int(skater_name)
                    skater_name = starts_in_event[skater_order - 1]

                except:
                    print("Not a valid input")

                skate_id = c.m.read_skate(event_number, skater_name)

                file_ids = c.m.read_file_id(skate_id)

                for each in file_ids:
                    print(each)

                file_id=input('which file id?: ')

                c.unload_file(file_id)

            case 'Q':
                running = False
            case _:
                c.v.err_invalid_input(action)

            
if __name__ == '__main__':
    __main__()
    
