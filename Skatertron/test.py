"""
from hypothesis import given
from hypothesis.strategies import text
"""

from competition_controller import Controller

controller = Controller()


def test_create_event():
    controller.create_event("69", "butts")
    controller.create_event("71","freeskate 9")

def test_read_event():
    for e in controller.read_event(event_number="69"):
        print(e.evt_title)
    print(controller.read_event())
    print(controller.read_event(event_id=65))
    print(controller.read_event(event_title='butts'))

def test_update_event():
    controller.update_event(1, "70", "butts")

def test_delete_event():
    controller.delete_event("69")
    controller.delete_event("71")


if __name__ == "__main__":
    'test_create_event()'
    test_read_event()
    test_update_event()
    'test_delete_event()'
