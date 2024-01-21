"""
from hypothesis import given
from hypothesis.strategies import text
"""

from competition_controller import Controller

controller = Controller()


def test_create_event():
    controller.create_event("69", "butts")
    controller.create_event("71","freeskate 9")
    controller.create_event("72","freeskate 10")


def test_read_all_events():
    print(controller.read_all_events())


def test_read_event_by_id():
    event = controller.read_event_by_id(84)

    print(event)
    print("ID:", event.id)
    print("#", event.evt_number)
    print("title:", event.evt_title)


def test_read_event_by_number():
    event = controller.read_event_by_number("70")

    print(event)
    print("ID:", event.id)
    print("#", event.evt_number)
    print("title:", event.evt_title)


def test_read_events_by_title():
    events = controller.read_events_by_title("t")
    for event in events:
        print(event)
        print("ID:", event.id)
        print("#", event.evt_number)
        print("title:", event.evt_title)


def test_update_event():
    controller.update_event(controller.read_event(event_number="70")[0].id, new_event_title="booty")


def test_delete_event():
    e = controller.read_event(event_title="freeskate 9")[0]
    controller.delete_event(event_id=e.id)
    controller.delete_event(event_number="69")
    controller.delete_event(event_title="freeskate 10")


if __name__ == "__main__":

    test_read_events_by_title()