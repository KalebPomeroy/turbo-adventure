#!/usr/bin/env python


def deep_merge(orig, other):
    """ Modify orig, overlaying information from other """

    for key, value in other.items():
        if key in orig and isinstance(orig[key], dict) and isinstance(value, dict):
            deep_merge(orig[key], value)
        else:
            orig[key] = value
