from model import ModelSQLite as model
from view import TUI as view
from pdf_scraper import PDF_Scraper as ps

from os import mkdir
from os.path import isdir, isfile

class Controller(object):
    
    def __init__(self, model, view):
        self.m = model
        self.v = view
        #self._valid_commands = self.valid_commands_setter()

        self.v.welcome()
        if not isdir('Competitions'):
            mkdir('Competitions')

    @property
    def valid_commands(self):
        return self._valid_commands

    '''
    def valid_commands_setter(self):

        match self.m.application_state:

            case 'init':
                self.valid_commands = {
                    'L': {
                        'Message': '[L]oad Competition',
                        'Function': self.load_competition(input('What is the event name?: '))
                        },
                    'N': {
                        'Message': '[N]ew Competition',
                        'Function': self.new_competition(input('What is the event name?: '))
                        }
                    }

        self.valid_commands.update({
            'Q': {
                    'Message': '[Q]uit',
                    'Function': exit()
                    }
            })
            
    '''

    def prompt_user(self):
        self.v.display_valid_actions(self.m.application_state)

    def load_competition(self, competition_name):
        if not isfile(f'Competitions\\{competition_name}.db'):
            self.v.err_not_exists('competition', competition_name)
        else:
            self.m.connection = f'{competition_name}'
            self.m.application_state = 'competition_loaded'
            self.v.load_comp(competition_name)
        
    def new_competition(self, competition_name):
        if isfile(f'Competitions\\{competition_name}.db'):
            self.v.err_item_exists('competition', competition_name)
        else:
            self.m.connection = f'{competition_name}'
            self.m.application_state = 'competition_loaded'
            self.v.new_comp(competition_name)

    def bulk_add_events(self, event_type):
        d = ps.get_dir_path()
        content_list = ps.bulk_stage_pdf(d)

        for event in content_list:
            skater_dict = {}
            if event_type == 'IJS' or event_type == 'i':
                skater_dict = ps.handle_ijs(event)
            elif event_type == '6.0':
                skater_dict = ps.handle_6_0(event)
            else:
                self.v.err_invalid_entry()

            self.m.create_event(skater_dict)
            self.v.disp_event(skater_dict['name'], skater_dict['skaters'])

    def add_event(self, event_type):
        f = ps.get_file_path()
        content = ps.stage_pdf(f)

        skater_dict = {}

        if event_type == 'IJS' or event_type == 'i':
            skater_dict = ps.handle_ijs(content)
        elif event_type == '6.0':
            skater_dict = ps.handle_6_0(content)
        else:
            self.v.err_invalid_entry()

        self.m.create_event(skater_dict)
        self.v.disp_event(skater_dict['name'], skater_dict['skaters'])
        
    def display_all_events(self):
        comp_name = self.m.comp_name
        events_list = self.m.read_all('events')
        
        self.v.disp_all_events(comp_name, events_list)

    def display_event_by_number(self, event_number):
        event_name = self.m.read_event_name(event_number)
        skater_list = self.m.read_skaters_in_event(event_number)

        self.v.disp_event(event_name, skater_list)

    def display_event_by_skater(self, skater):
        events_list = self.m.read_events_by_skater(skater)

        self.v.disp_events_by_skater(skater, events_list)
        
    '''
    mvp:
    - add event
    - get all events
    - get events by skater
    - get files by skate
    - delete event
    - attach file
    - state
    - command mapping
    
    '''

def __main__():
    running = True
    
    while running:
        c.prompt_user()

        try:
            action = input().upper()
        except:
            print('Invalid entry')
        
        match action:            
            
            case 'L':
                comp_name = input('What is the event name?: ')
                c.load_competition(comp_name)
            case 'N':
                comp_name = input('What is the event name?: ')
                c.new_competition(comp_name)
            case 'B':
                event_type = input('IJS or 6.0: ')
                c.bulk_add_events(event_type)
            case 'A':
                event_type = input('IJS or 6.0: ')
                c.add_event(event_type)
            case 'D':
                flag_type = input('[A]ll events | Event by [N]umber | Events by [S]kater: ')
                match flag_type:
                    case 'A':
                        c.display_all_events()
                    case 'N':
                        event_number = input('What is the event number?: ').zfill(3)
                        c.display_event_by_number(event_number)
                    case 'S':
                        skater_name = input('Which Skater?: ')
                        c.display_event_by_skater(skater_name)
                        
            case 'F':
                #attach files
                pass
            case 'U':
                #unload files
                pass
            case 'Q':
                running = False
            case _:
                c.v.err_invalid_input(action)
            

            
if __name__ == '__main__':
    
    c = Controller(model(), view())

    __main__()
    
