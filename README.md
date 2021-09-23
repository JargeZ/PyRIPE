# PyRIPE

This project did not achive first version, but you can use it and modify it.\
The original architecture and tests are implemented here. You are open to expanding functionality.

If you will work and maintain this library, you can contact me for help.

## Usage
Main class is RipeApi
```python
rapi = RipeApi(
    password='YOU RIPE PASSWORD', 
    test_database=True, # Use rest-test.db.ripe.net instead of rest.db.ripe.net
    dry_run=False # Add dry-run parameter to request, which sended to api endpoint. Might be useful to test scripts on production database
)
```

api class provide methods to build objects and manipulate database.

### rapi.create_person()
```python
def create_person(self, name: str, 
                        address: str, 
                        phone: str, 
                        email: str, 
                        maintainer: str) -> Person:

new_person = rapi.create_person( ... )
```
The `maintainer` param should be valid RIPE mnt-er. Example for test database it is `"TEST-NCC-HM-MNT"`

Returns Person object, this is pydantic model of json representation of RIPE object.

> Each object have primary key, named nic_hdl.nic_hdl\
> It used for GET/DELETE request.

### rapi.get_person() / rapi.delete_person()
`Person.key` encapsulate nic_hdl key for an object.
```python
rapi.delete_person(nic_hdl=new_person.key)
```
Returns deleted object (REST style)

---

Another architecture for organisation.
Here we need to create organisation object before API call.
```python
org = NewOrganisation(
            org_name="Test Organ",
            address="Pushkina string, Moscow, Russia",
            phone='+7 999 666 8228',
            e_mail="jargez@ph3.ru",
            maintainer="TEST-NCC-HM-MNT"
        )
```
where `NewOrganisation` is pydantic model
And after that call 
```
new_org = rapi.create_organization(org)
```
nic_hdl key - new_org.key

Also yoy can get any attr of RIPE object with get_attr method
```python
org_name = new_org.get_attr('org-name')
```
---
## For more example see tests and source code.
In the future, it is necessary to bring the creation of objects to a single style by pidantic model
