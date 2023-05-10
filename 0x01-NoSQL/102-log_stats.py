#!/usr/bin/env python3
"""Get info from nginx logs."""
from pymongo import MongoClient


def main():
    """Print some data from nginx logs."""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx = client.logs.nginx
    print("{} logs".format(nginx.count_documents({})))
    print("Methods:")
    for method in methods:
        print(
            "\tmethod {}: {}".format(
                method,
                nginx.count_documents({"method": method}),
            )
        )

    print("{} status check".format(
        nginx.count_documents({"method": "GET", "path": "/status"}),
    ))

    print("IPs:")
    for ip in nginx.aggregate([
            {"$group": {
                "_id": {"ip": "$ip"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
    ]):
        print("\t{}: {}".format(ip.get("_id").get("ip"), ip.get("count")))


if __name__ == '__main__':
    main()
