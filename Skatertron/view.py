line_length = 120

def message_wrap(func):
    def wrap(*args, **kwargs):
        message = '/' * line_length + '\n'
        message += func(*args, **kwargs)
        message += '\n'+'/' * line_length

        message_list = message.split('\n')
        print()
        for line in message_list:
            print(line.center(line_length))
        print()

    return wrap
        


class TUI(object):
    @staticmethod
    @message_wrap
    def welcome():
        return('Welcome to the LMP Skatertron')

    @staticmethod
    @message_wrap
    def new_comp(competition):
        return(f'Initialized new competition {competition}')

    @staticmethod
    @message_wrap
    def load_comp(competition):
        return(f'Loaded competition {competition}')

    @staticmethod
    @message_wrap
    def save_comp():
        return(f'Saved all data!')

    @staticmethod
    @message_wrap
    def unload_comp_message():
        return(f'Cleared current competition')

    @staticmethod
    @message_wrap
    def disp_event(evt_title, skater_list):
        message = f'{evt_title}\nSKATERS\n\n'

        i = 1
        for skater in skater_list:
            message += f'{i}. {skater}\n'
            i += 1

        return(message)

    @staticmethod
    @message_wrap
    def disp_event_with_files(evt_title, files_dict):
        message = f'{evt_title}\nSKATERS & FILES\n\n'

        skaters = files_dict.keys()

        print(skaters)

        i = 1
        for skater in skaters:
            message += f'{i}. {skater}:\n'

            if type(files_dict[skater]) == list:
                for file in files_dict[skater]:
                    message += f"--- {file}\n"
            else:
                message += f"--- {files_dict[skater]}\n"
            i += 1

        return(message)


    @staticmethod
    @message_wrap
    def disp_all_events(comp, evt_list):
        message = f'{comp}\nALL EVENTS\n\n'

        i = 1
        for e in evt_list:
            message += f'Event {e[1]}: {e[2]}\n'

        return(message)

    @staticmethod
    @message_wrap
    def disp_events_by_skater(skater, evt_list):
        message = f'{skater} competed in:\n\n'

        i = 1
        for e in evt_list:
            print(e)
            message += f'{e[0]}: {e[1]}\n'

        return(message)
    
    @staticmethod
    @message_wrap
    def rename(item, old_name, new_name):
        message = f'{item} {old_name} renamed to {new_name}'

        return(message)

    @staticmethod
    @message_wrap
    def err_not_exists(item_type, item):
        message = f'ERROR: {item_type} {item} does not exist!'

        return(message)

    @staticmethod
    @message_wrap
    def err_item_exists(item_type, item):
        message = f'ERROR: {item_type} {item} already exists!'

        return(message)

    @staticmethod
    @message_wrap
    def err_unknown_input(command):
        message = f'ERROR: {command} is not a recognized command!'

        return(message)

    @staticmethod
    @message_wrap
    def err_invalid_input(command):
        message = f'ERROR: {command} is not a valid command in the current state!'

        return(message)

    @staticmethod
    @message_wrap
    def err_invalid_entry():
        message = 'ERROR: This command cannot be executed as entered!'

        return(message)

    @staticmethod
    def display_valid_actions(app_state):
        match app_state:
            case 'init':
                message = '[L]oad competition | [N]ew competition?'
            case 'competition_loaded':
                message = '[B]ulk add events | [A]dd single event | [D]isplay event(s) | Attach [F]iles'

        message += ' | [Q]uit'

        print(message)

    @staticmethod
    @message_wrap
    def add_file(event_number, skater, file):
        message = f'Added {file} to {skater}\'s skate on event #{event_number}'

        return(message)


if __name__ == '__main__':
    event_title = "001 Freeskate 5 Short Program"
    skater_list = ["aSsdfkjl", "akljljklkjqww"]
    files_dick = {"Sarah Blasdfkn": ["01532.mp4", "sdfasd.jpg"], "Johnathan SFJSDLJKSFD": ["01324.mov", "12230.jpg", "asdfasf.jpg"]}

    TUI.welcome()
    TUI.load_comp("VAIL 2023")
    
    TUI.disp_event(event_title, skater_list)
    TUI.disp_event_with_files(event_title, files_dick)

    TUI.rename('skater', 'chocho wowie', 'chaha maui')
    
