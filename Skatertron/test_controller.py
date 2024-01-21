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
    print(controller.read_event())

def test_read_event_id_by_number():
    print(controller.read_event_id(controller.read_event(event_number="71")))

def test_update_event():
    controller.update_event(controller.read_event(event_number="70")[0].id, new_event_title="booty")


def test_delete_event():
    e = controller.read_event(event_title='freeskate 9')[0]
    controller.delete_event(event_id=e.id)
    controller.delete_event(event_number="69")
    controller.delete_event(event_title='freeskate 10')


if __name__ == "__main__":
    test_read_event_id_by_number()
