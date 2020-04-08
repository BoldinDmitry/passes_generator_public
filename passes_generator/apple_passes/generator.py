import hashlib
import json
import subprocess
import zipfile
from io import BytesIO

from passes_generator.config import (
    APPLE_CERTIFICATE,
    APPLE_KEY,
    APPLE_PASSWORD,
    APPLE_WWDR,
)


class ApplePassKitGenerator:
    def __init__(
        self,
        resource,
        wwdr: str = APPLE_WWDR,
        certificate: str = APPLE_CERTIFICATE,
        key: str = APPLE_KEY,
        password=APPLE_PASSWORD,
    ):
        """
        Generator for Apple Passes
        :param wwdr: path to file with wwdr
        :param certificate: path to file with certificate
        :param key: path to file with key
        :param password: string with password
        :param resource: resource object
        """
        self.wwdr = wwdr
        self.certificate = certificate
        self.key = key
        self.password = password

        resource.do_checks()
        self.resource = resource.json.encode("UTF-8")

        self._files = {}

    @staticmethod
    def sha1(file_data: bytes) -> str:
        sha1sum = hashlib.sha1(file_data)
        return sha1sum.hexdigest()

    def add_file(self, filename: str, data: bytes):
        """
        Add file to Apple Pass
        """
        self._files[filename] = data

    def _create_manifest(self) -> bytes:
        """
        Create manifest from given resources and files.
        This function should be called after all files were added.
        """
        manifest = {"pass.json": self.sha1(self.resource)}
        for filename, data in self._files.items():
            manifest[filename] = self.sha1(data)
        print(json.dumps(manifest).encode("utf-8"))
        return json.dumps(manifest).encode("utf-8")

    def _create_signature(self, manifest: bytes) -> bytes:
        """
        Signature file creation
        """
        smime_cmd = [
            "openssl",
            "smime",
            "-binary",
            "-sign",
            "-certfile",
            self.wwdr,
            "-signer",
            self.certificate,
            "-inkey",
            self.key,
            "-outform",
            "DER",
            "-passin",
            "pass:{}".format(self.password),
        ]
        print(smime_cmd)
        process = subprocess.Popen(
            smime_cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )

        process.stdin.write(manifest)
        signature, error = process.communicate()
        if process.returncode != 0:
            raise Exception(error)
        return signature

    def _create_zip(self, signature: bytes, manifest: bytes, buffer: BytesIO):
        """
        Zip all files and create Loyalty card
        :param signature: file with signature
        :param manifest: file with manifest
        :param buffer: buffer, where zip with card will be saved
        """
        zip_pass = zipfile.ZipFile(buffer, "w")
        zip_pass.writestr("signature", signature)
        zip_pass.writestr("manifest.json", manifest)
        zip_pass.writestr("pass.json", self.resource)
        for filename, data in self._files.items():
            zip_pass.writestr(filename, data)
        zip_pass.close()

    def create(self, buffer: BytesIO = None) -> BytesIO:
        """
        Apple Loyalty card creation
        This function should be called after all files were added.
        :param buffer: buffer, where card will be saved
        :return: buffer with card
        """
        if not buffer:
            buffer = BytesIO()
        manifest = self._create_manifest()
        signature = self._create_signature(manifest)
        self._create_zip(signature, manifest, buffer)
        buffer.seek(0)
        return buffer
