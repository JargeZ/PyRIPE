from typing import TypedDict, Optional, Literal

from lib.Exceptions import RipeApiException, NoEntriesFound
from lib.SessionWithUrlBase import SessionWithUrlBase
from lib.logs import logger_wraps, interpolate_error_message
from models.InetNum import InetNum
from models.Organisation import Organisation, NewOrganisation
from models.Person import Person
from models.common import Source, Attribute
from loguru import logger


class RipeApi:
    def __init__(self, password='emptypassword', test_database=True, dry_run=False):
        params = {
            'password': password,
            'dry-run': dry_run
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if test_database:
            self._source = "TEST"
            baseurl = "https://rest-test.db.ripe.net/test/"
        else:
            self._source = "RIPE"
            baseurl = "https://rest.db.ripe.net/ripe/"

        self.session = SessionWithUrlBase(url_base=baseurl)
        self.session.params.update(params)
        self.session.headers.update(headers)

    @logger_wraps()
    def _get(self, *args, **kwargs):
        logger.debug(f"_get()")
        response = self.session.get(*args, **kwargs)
        self._response_is_valid(response)

        return response.json()

    def build_person(self, name: str, address: str, phone: str, email: str, maintainer: str) -> dict:
        attributes = [
            Attribute(name='person', value=name),
            Attribute(name='address', value=address),
            Attribute(name='phone', value=phone),
            Attribute(name='e-mail', value=email),
            Attribute(name='mnt-by', value=maintainer),
            Attribute(name='nic-hdl', value='AUTO-1'),
            Attribute(name='remarks', value='remark'),
            Attribute(name='source', value=self._source),
        ]
        new_person = {
            'source': Source(id=self._source).dict(exclude_none=True),
            'attributes': {
                'attribute': [attr.dict(exclude_none=True) for attr in attributes]
            },
        }

        return new_person

    # TODO: WARNING: wip code
    def build_organization(self, *args, **kwargs: dict[str, str]) -> dict:
        if 'organisation' not in kwargs:
            kwargs['organisation'] = 'AUTO-1'

    @logger_wraps()
    def _delete(self, *args, **kwargs):
        logger.debug(f"_get()")
        response = self.session.delete(*args, **kwargs)
        self._response_is_valid(response)

        return response.json()

    @logger_wraps()
    def _post(self, *args, **kwargs):
        response = self.session.post(*args, **kwargs)
        self._response_is_valid(response)

        return response.json()

    @logger_wraps()
    def _put(self, *args, **kwargs):
        response = self.session.put(*args, **kwargs)
        self._response_is_valid(response)

        return response.json()

    @staticmethod
    def _response_is_valid(res) -> None:
        try:
            response = res.json()
        except Exception as e:
            raise RipeApiException(reason=e, message=str(e))

        if response.get('errormessages', None):
            for error in response['errormessages']['errormessage']:
                if error['severity'] == 'Info':
                    logger.info(error["text"])
                elif 'ERROR:101:' in error['text']:
                    raise NoEntriesFound(interpolate_error_message(error))
                else:
                    raise RipeApiException(interpolate_error_message(error))

        # TODO: but if no one objet?
        if len(response['objects']['object']) > 1:
            raise RipeApiException(f"More than one object returned")

    def get_inetnum(self, inetnum):
        res = self._get(f'inetnum/{inetnum}')

        return InetNum.parse_obj(res['objects']['object'][0])

    def get_person(self, nic_hdl) -> Person:
        res = self._get(f'person/{nic_hdl}')

        return Person.parse_obj(res['objects']['object'][0])

    def delete_person(self, nic_hdl) -> Person:
        res = self._delete(f'person/{nic_hdl}')
        return Person.parse_obj(res['objects']['object'][0])

    def create_person(self, name: str, address: str, phone: str, email: str, maintainer: str) -> Person:
        new_person = self.build_person(name=name, address=address, phone=phone, email=email, maintainer=maintainer)

        post_json = {
            'objects': {
                'object': [new_person]
            }
        }
        person = self._post('person', json=post_json)['objects']['object'][0]

        person = Person.parse_obj(person)
        logger.info(f"Created Person with nic_hdl={person.key}")
        return person

    def delete_organisation(self, organisation) -> Organisation:
        res = self._delete(f'organisation/{organisation}')
        return Organisation.parse_obj(res['objects']['object'][0])

    def create_organization(self, org: NewOrganisation) -> Organisation:
        org.obj['source'] = self._source

        post_json = {
            'objects': {
                'object': [org.get()]
            }
        }
        returned_object = self._post('organisation', json=post_json)['objects']['object'][0]

        returned_object = Organisation.parse_obj(returned_object)
        logger.info(f"Created Person with nic_hdl={returned_object.key}")
        return returned_object
