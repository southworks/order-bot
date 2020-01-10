# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class Unit:
    """ TODO: Add description for Unit class. """

    def __init__(self, unit_id: int = 0, description: str = ""):
        self.unit_id = unit_id
        self.description = description

    def to_string(self):
        """ returns a text representation of the object """
        return "{0} {1}".format(self.unit_id, self.description)
