from pydantic import BaseModel, Field

from models.common import Link, Source, Attributes


class InetNum(BaseModel):
    type: str = 'inetnum'
    link: Link
    source: Source
    primary_key: Attributes = Field(alias='primary-key')
    attributes: Attributes


if __name__ == '__main__':
    json = """
{
    "type": "inetnum",
    "link": {
        "type": "locator",
        "href": "https://rest.db.ripe.net/ripe/inetnum/84.23.56.0 - 84.23.63.255"
    },
    "source": {
        "id": "ripe"
    },
    "primary-key": {
        "attribute": [
            {
                "name": "inetnum",
                "value": "84.23.56.0 - 84.23.63.255"
            }
        ]
    },
    "attributes": {
        "attribute": [
            {
                "name": "inetnum",
                "value": "84.23.56.0 - 84.23.63.255"
            },
            {
                "name": "netname",
                "value": "RU-DATALINE-20041012"
            },
            {
                "name": "country",
                "value": "RU"
            },
            {
                "link": {
                    "type": "locator",
                    "href": "https://rest.db.ripe.net/ripe/organisation/ORG-DL76-RIPE"
                },
                "name": "org",
                "value": "ORG-DL76-RIPE",
                "referenced-type": "organisation"
            },
            {
                "link": {
                    "type": "locator",
                    "href": "https://rest.db.ripe.net/ripe/person/AAB155-RIPE"
                },
                "name": "admin-c",
                "value": "AAB155-RIPE",
                "referenced-type": "person"
            },
            {
                "link": {
                    "type": "locator",
                    "href": "https://rest.db.ripe.net/ripe/role/DTLN1-RIPE"
                },
                "name": "tech-c",
                "value": "DTLN1-RIPE",
                "referenced-type": "role"
            },
            {
                "name": "status",
                "value": "ALLOCATED PA"
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
                "link": {
                    "type": "locator",
                    "href": "https://rest.db.ripe.net/ripe/mntner/RIPE-NCC-HM-MNT"
                },
                "name": "mnt-by",
                "value": "RIPE-NCC-HM-MNT",
                "referenced-type": "mntner"
            },
            {
                "name": "created",
                "value": "2020-05-04T11:27:27Z"
            },
            {
                "name": "last-modified",
                "value": "2020-05-04T11:27:27Z"
            },
            {
                "name": "source",
                "value": "RIPE"
            }
        ]
    }
}"""
    inum = InetNum.parse_raw(json)
    print(inum)
