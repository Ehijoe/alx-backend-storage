#!/usr/bin/env python3
"""Update a document."""


def update_topics(mongo_collection, name, topics):
    """Update the list of topics treated by a school."""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
