import json

from passes_generator.google_passes.resources import (
    GoogleObjectResources,
    GoogleClassResources,
)
import passes_generator.config as config
from passes_generator.google_passes.generator import (
    GoogleClassGenerator,
    GoogleObjectGenerator,
)
from uuid import uuid4

if __name__ == "__main__":
    class_id = f"{config.GOOGLE_ISSUER_ID}.LOYALTY_CLASS_{str(uuid4())}"
    class_res = {
        # required fields
        "id": class_id,
        "issuerName": "BURGER PUB",
        "programName": "KVADRAT",
        "programLogo": {
            "kind": "walletobjects#image",
            "sourceUri": {
                "kind": "walletobjects#uri",
                "uri": "https://s-soboy.com/mediafiles/cafe_5/item_photo_None-icon.png",
            },
        },
        "reviewStatus": "UNDER_REVIEW",
        # optional
        "hexBackgroundColor": "#000000",
        "heroImage": {
            "sourceUri": {
                "uri": "https://s-soboy.com/mediafiles/cafe_5/item_photo_18-Screenshot_2020-03-13_at_16.30.10.png",
            },
        },

        "linksModuleData": {
            "uris": [
                {
                    "kind": "walletobjects#uri",
                    "uri": "https://goo.gl/maps/GUyK4v3uEv1cwBQY8",
                    "description": "Наш адрес",
                },
                {
                    "kind": "walletobjects#uri",
                    "uri": "tel:+78126791008",
                    "description": "Позвонить в ресторан",
                },
                {
                    "kind": "walletobjects#uri",
                    "uri": "https://www.instagram.com/pub_kvadrat_spb/",
                    "description": "Наш инстаграм",
                }
            ]
        },
        "locations": [
            {
                "kind": "walletobjects#latLongPoint",
                "latitude": 59.9111999,
                "longitude": 30.2706328,
            },
        ],
    }

    obj_id = f"{config.GOOGLE_ISSUER_ID}.{str(uuid4())}"
    obj_res = {
        # required fields
        "id": obj_id,
        "classId": class_id,
        "state": "active",
        # optional
        "barcode": {"type": "qrCode", "value": "28343E3"},
    }

    class_res_obj = GoogleClassResources(class_res)
    obj_res_obj = GoogleObjectResources(obj_res)

    class_generator = GoogleClassGenerator(
        class_res_obj, config.GOOGLE_SERVICE_ACCOUNT_PATH, config.GOOGLE_SCOPES
    )
    class_generator.create_class()

    print(class_generator.resource["id"])

    obj_generator = GoogleObjectGenerator(
        obj_res_obj, config.GOOGLE_SERVICE_ACCOUNT_PATH, config.GOOGLE_SCOPES
    )
    jwt = obj_generator.create_class()

    save_link = "https://pay.google.com/gp/v/save/"
    print(save_link + jwt)
