class TUI(object):

    @staticmethod
    def disp_event(evt_title, skater_list):
        print(f'--- {evt_title} ---')
        print(f'--- SKATERS ---\n')

        i = 1
        for skater in skater_list:
            print(f"{i}. {skater}")
            i += 1

    @staticmethod
    def disp_event_with_files(evt_title, files_dict):
        print(f'--- {evt_title} ---')
        print(f'--- SKATERS & FILES ---\n')

        skaters = files_dict.keys()

        i = 1
        for skater in skaters:
            print(f"{i}. (skater):")
            video = None
            photos = []
            for file in files_dict[skater]:
                print(f"--- {file}")
            i += 1
                
            

if __name__ == '__main__':
    event_title = "001 Freeskate 5 Short Program"
    skater_list = ["aSsdfkjl", "akljljklkjqww"]
    files_dick = {"Sarah Blasdfkn": ["01532.mp4", "sdfasd.jpg"], "Johnathan SFJSDLJKSFD": ["01324.mov", "12230.jpg"]}
    
    TUI.disp_event(event_title, skater_list)
    TUI.disp_event_with_files(event_title, files_dick)
