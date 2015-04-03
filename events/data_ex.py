# Author: Noah Gold


class EventDetails:
    """
    Contains event details.
    """

    def __init__(self, title, message):
        self.title = title
        self.message = message

    def __eq__(self, other):
        if isinstance(other, EventDetails):
            return self.title == other.title and self.message == self.message

    def __ne__(self, other):
        return not self.__eq__(other)
