from typing import Optional

from pydantic import BaseModel, Field

from lib.Exceptions import RipeApiException
from models.Person import Person
from models.common import Link, Source, Attributes, BaseRipeModel, Attribute


class Organisation(BaseRipeModel):
    type: str = 'organisation'


class NewOrganisation:
    def __init__(self, *args,
                 organisation: str = 'AUTO-1',
                 org_name: str,
                 org_type: str = "OTHER",
                 address: str,
                 phone: str,
                 e_mail: str,
                 maintainer: Optional[str] = None,
                 mnt_by: Optional[str] = None,
                 mnt_ref: Optional[str] = None,
                 **kwargs,
                 ):
        if not maintainer and not (mnt_by and mnt_ref):
            raise RipeApiException("maintainer or (mnt_by and mnt_ref) ust be specify")

        if not mnt_by:
            mnt_by = maintainer
        if not mnt_ref:
            mnt_ref = maintainer

        self.obj = {
            'organisation': organisation,
            'org_name': org_name,
            'org_type': org_type,
            'address': address,
            'phone': phone,
            'e_mail': e_mail,
            'mnt_by': mnt_by,
            'mnt_ref': mnt_ref,
            **kwargs,
        }

    def get(self):
        attributes = []

        for name, value in self.obj.items():
            name = name.replace('_', '-')
            attributes.append(
                Attribute(name=name, value=value)
            )

        return {
            'attributes': {
                'attribute': [attr.dict(exclude_none=True) for attr in attributes]
            },
        }

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
    inum = Person.parse_raw(json)
    print(inum)
