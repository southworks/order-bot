# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class Action:
    """ TODO: Add description for Action class. """
    def execute(self, number, order, item):
        raise NotImplementedError


class Add(Action):
    """ TODO: Add description for Add class. """
    def execute(self, number, order, item):
        pass


class Remove(Action):
    """ TODO: Add description for Remove class. """
    def execute(self, number, order, item):
        pass


class Confirm(Action):
    """ TODO: Add description for Confirm class. """
    def execute(self, number, order, item):
        pass
