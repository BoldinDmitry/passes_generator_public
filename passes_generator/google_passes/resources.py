from passes_generator.resource_generator import AbstractResources


class GoogleClassResources(AbstractResources):
    required_fields = {"programName", "programLogo", "id", "issuerName", "reviewStatus"}


class GoogleObjectResources(AbstractResources):
    required_fields = {"id", "classId", "state"}
