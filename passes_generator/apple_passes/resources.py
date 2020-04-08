import json

from passes_generator.resource_generator import AbstractResources


class ApplePassResources(AbstractResources):
    required_fields = {
        "description",
        "formatVersion",
        "organizationName",
        "passTypeIdentifier",
        "serialNumber",
        "teamIdentifier",
    }
