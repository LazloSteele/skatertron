"""
from hypothesis import given
from hypothesis.strategies import text
"""

from competition_controller import EventController, SkateController

e_c = EventController()
s_c = SkateController()


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
    print("#", event.evt_number)
    print("title:", event.evt_title)


def test_read_event_by_number():
    event = e_c.read_event_by_number("70")

    print(event)
    print("ID:", event.id)
    print("#", event.evt_number)
    print("title:", event.evt_title)


def test_read_events_by_title():
    events = e_c.read_events_by_title("t")
    for event in events:
        print(event)
        print("ID:", event.id)
        print("#", event.evt_number)
        print("title:", event.evt_title)


def test_update_event():
    e_c.update_event(e_c.read_event_by_number("70").id, new_event_title="booty")


def test_delete_event():
    e = e_c.read_event_by_number("freeskate 9")
    e_c.delete_event(e.id)


def test_create_skate():
    s_c.create_skate(85, "Shanda Rhymes")


def test_read_all_skates():
    print(s_c.read_all_skates())


def test_read_skate_by_id():
    skate = s_c.read_skate_by_id(1)
    event_title = e_c.read_event_by_id(skate.evt_id).evt_title
    print(skate)
    print("ID:", skate.id)
    print(skate.skater, "skating in", event_title)


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


if __name__ == "__main__":
    pass
