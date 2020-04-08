import passes_generator.config as config
import time

from google.auth import crypt as crypt_google
from google.auth import jwt as jwt_google


class GooglePassJwt:
    def __init__(self):
        self.audience = config.GOOGLE_AUDIENCE
        self.type = config.GOOGLE_JWT_TYPE
        self.iss = config.GOOGLE_SERVICE_ACCOUNT_EMAIL_ADDRESS
        self.origins = config.ORIGINS
        self.iat = int(time.time())
        self.payload = {}

        self.signer = crypt_google.RSASigner.from_service_account_info(
            config.GOOGLE_SERVICE_ACCOUNT_INFO
        )

    def add_loyalty_class(self, resource_payload):
        self.payload.setdefault("loyaltyClasses", [])
        self.payload["loyaltyClasses"].append(resource_payload)

    def add_loyalty_object(self, resource_payload):
        self.payload.setdefault("loyaltyObjects", [])
        self.payload["loyaltyObjects"].append(resource_payload)

    def generate_unsigned_jwt(self):
        unsigned_jwt = {
            "iss": self.iss,
            "aud": self.audience,
            "typ": self.type,
            "iat": self.iat,
            "payload": self.payload,
            "origins": self.origins,
        }

        return unsigned_jwt

    def generate_signed_jwt(self):
        jwtToSign = self.generate_unsigned_jwt()
        signed_jwt = jwt_google.encode(self.signer, jwtToSign)

        return signed_jwt
