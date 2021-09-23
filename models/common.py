from typing import Optional

from pydantic import BaseModel, Field


class Link(BaseModel):
    type: str
    href: str


class Source(BaseModel):
    id: str


class Attribute(BaseModel):
    name: str
    value: str
    link: Optional[Link]
    referenced_type: Optional[str] = Field(alias='referenced-type')


class Attributes(BaseModel):
    attribute: list[Attribute]


class BaseRipeModel(BaseModel):
    primary_key: Attributes = Field(alias='primary-key')
    attributes: Attributes
    link: Optional[Link]
    source: Optional[Source]

    def get_attr(self, attr_name, default=False):
        for attr in self.attributes.attribute:
            if attr.name == attr_name:
                return attr.value

        if default is False:
            return default

        raise KeyError(f"attr_name not found in {str(self)}")

    @property
    def key(self):
        return self.primary_key.attribute[0].value
