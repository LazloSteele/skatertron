# to prevent duplicate competitions
class CompExists(Exception):
    pass

# to prevent duplicate event entries
class EventExists(Exception):
    pass

# to prevent duplicate skate entries
class SkaterExistsInEvent(Exception):
    pass

# to handle bad lookups
class EventNotExists(Exception):
    pass

class SkaterNotInEvent(Exception):
    pass
