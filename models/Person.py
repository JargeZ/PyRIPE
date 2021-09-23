from typing import Optional

from pydantic import BaseModel, Field

from models.common import Link, Source, Attributes, BaseRipeModel


class Person(BaseRipeModel):
    type: str = 'person'


class NewPerson():
    def __init__(self):
        pass


if __name__ == '__main__':
    json = """
{
    "type": "person",
    "link": {
        "type": "locator",
        "href": "https://rest.db.ripe.net/ripe/person/AAB155-RIPE"
    },
    "source": {
        "id": "ripe"
    },
    "primary-key": {
        "attribute": [
            {
                "name": "nic-hdl",
                "value": "AAB155-RIPE"
            }
        ]
    },
    "attributes": {
        "attribute": [
            {
                "name": "person",
                "value": "Alexey A Bagaev"
            },
            {
                "name": "address",
                "value": "Borovaya 7/10, Moscow, Russia"
            },
            {
                "name": "phone",
                "value": "+7 495 7846505"
            },
            {
                "name": "nic-hdl",
                "value": "AAB155-RIPE"
            },
            {
                "link": {
                    "type": "locator",
                    "href": "https://rest.db.ripe.net/ripe/mntner/DTLN-MNT"
                },
                "name": "mnt-by",
                "value": "DTLN-MNT",
                "referenced-type": "mntner"
            },
            {
                "name": "created",
                "value": "2011-03-16T12:13:13Z"
            },
            {
                "name": "last-modified",
                "value": "2011-03-16T12:13:13Z"
            },
            {
                "name": "source",
                "value": "RIPE"
            }
        ]
    }
}"""
    inum: Person = Person.parse_raw(json)
    print(inum)
