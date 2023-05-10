#!/usr/bin/env python3
"""Top students."""


def top_students(mongo_collection):
    """Return a list of the top students."""
    students = mongo_collection.aggregate([
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
    return list(students)
