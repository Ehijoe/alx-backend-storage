#!/usr/bin/env python3
"""Insert a document."""


def insert_school(mongo_collection, **kwargs):
    """Insert a document into a collection."""
    return mongo_collection.insert_one(kwargs).inserted_id
