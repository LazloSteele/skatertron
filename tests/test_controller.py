from competition_controller import EventController, SkateController, FileController

e_c = EventController()
s_c = SkateController()
f_c = FileController()


def test_create_event():
    e_c.create_event("69", "butts")
    e_c.create_event("71", "freeskate 9")
    e_c.create_event("72", "freeskate 10")


def test_read_all_events():
    print(e_c.read_all_events())


def test_read_event_by_id():
    event = e_c.read_event_by_id(84)

    print(event)
    print("ID:", event.id)
    print("#", event.event_number)
    print("title:", event.event_name)


def test_read_event_by_number():
    event = e_c.read_event_by_number("70")

    print(event)
    print("ID:", event.id)
    print("#", event.event_number)
    print("title:", event.event_name)


def test_read_events_by_title():
    events = e_c.read_events_by_title("t")
    for event in events:
        print(event)
        print("ID:", event.id)
        print("#", event.event_number)
        print("title:", event.event_name)


def test_update_event():
    e_c.update_event(e_c.read_event_by_number("70").id, new_event_title="booty")


def test_delete_event():
    e = e_c.read_event_by_number("freeskate 9")
    e_c.delete_event(e.id)


def test_create_skate():
    s_c.create_skate(85, "Ira Glass")
    s_c.create_skate(85, "John Bahm")


def test_read_all_skates():
    print(s_c.read_all_skates())


def test_read_skate_by_id():
    skate = s_c.read_skate_by_id(1)
    event_title = e_c.read_event_by_id(skate.event_id).event_name
    print(skate)
    print("ID:", skate.id)
    print(skate.skater_name, "skating in", event_title)


def test_read_skates_by_event():
    skates = s_c.read_skates_by_event(84)
    for skate in skates:
        print(skate)


def test_read_skates_by_skater():
    skates = s_c.read_skates_by_skater("Shanda Rhymes")
    for skate in skates:
        print(skate)


def test_update_skate():
    s_c.update_skate(1, new_skater_name="Ira Glass")


def test_delete_skate():
    s_c.delete_skate(4)


def test_create_file():
    f_c.create_file(6, f"/competitions/{f_c.competition}/assets/003.txt")
    f_c.create_file(7, f"/competitions/{f_c.competition}/assets/004.txt")


def test_read_all_files():
    print(f_c.read_all_files())


def test_read_files_by_skate():
    files = f_c.read_files_by_skate(5)
    for file in files:
        print(file)
        print(file.id)
        print(e_c.read_event_by_id(s_c.read_skate_by_id(file.skate_id).event_id).event_name)
        print(file.file_name)


def test_read_file_by_id():
    print(f_c.read_file_by_id(1))


def test_read_file_by_skater_name():
    print(f_c.read_files_by_skater_name("Ira Glass"))


def test_update_file():
    f_c.update_file(1, new_skate_id=6, new_filepath=f"/competitions/{f_c.competition}/assets/001.txt")


def test_delete_file():
    f_c.delete_file(1)


if __name__ == "__main__":
    test_read_all_files()
    test_read_all_files()
