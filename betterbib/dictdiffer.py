# -*- coding: utf-8 -*-
#


def adds_info(entry0, entry1):
    '''Returns True if entry1 adds information to entry0, False otherwise.
    '''
    entry0u = _to_uppercase_keys(entry0)
    entry1u = _to_uppercase_keys(entry1)
    d = DictDiffer(entry0u, entry1u)
    # print(d.added())
    # print(d.removed())
    # print(d.unchanged())
    # Count as same if no entries were added or changed.
    return d.changed() or d.added()


def _to_uppercase_keys(dictionary):
    '''Returns a str-keyed dictionary with uppercase keys.
    '''
    new_dict = {}
    for key, value in dictionary.iteritems():
        new_dict[key.upper()] = value
    return new_dict


# from <http://stackoverflow.com/a/1165552/353337>
class DictDiffer(object):
    '''
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    '''
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = \
            set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(
            o for o in self.intersect
            if self.past_dict[o] != self.current_dict[o]
            )

    def unchanged(self):
        return set(
            o for o in self.intersect
            if self.past_dict[o] == self.current_dict[o]
            )
