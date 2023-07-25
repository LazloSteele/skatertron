import os

class controller():

    @staticmethod
    def NEW_COMP(model):
        
        dir_list = [n for n in os.listdir() if os.path.isdir(n)]

        for level in ["IJS","6.0"]:
            my_path = next(n for n in dir_list if level in n)
            my_list = [n for n in os.listdir(my_path) if n.endswith(".pdf")]

            for pdf in my_list:
                model.handle_pdf(f"{my_path}/{pdf}", level)

    @staticmethod
    def GET_EVENTS(model):
        return model.get_events()

    @staticmethod
    def SET_SERVER(model, con):
        model.set_server(con)
                
    def ADD_EVENT(self, evt_number, evt_name):
        m.events.append({f"({evt_number.zfill(3)}) {evt_name.upper()}":[]})
    
    def DEL_COMP(model):
        model.delete()

    def REN_EVENT(self):
        pass

    def ADD_SKATER(self):
        pass

    def DEL_SKATER(self):
        pass

    def REN_SKATER(self):
        pass


