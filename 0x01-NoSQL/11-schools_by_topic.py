#!/usr/bin/env python3
"""Find the schools that teach python."""


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools that teach python."""
    return list(mongo_collection.find({"topics": topic}))
