import json
import abc


class AbstractResources(dict, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    @staticmethod
    def _json_serializable(x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            raise ValueError(f"Object with type {type(x)} is not JSON serializable")

    @property
    def json(self):
        return json.dumps(self)

    @property
    @abc.abstractmethod
    def required_fields(self):
        """
        This field must be overwritten by list of required fields
        """
        pass

    def do_checks(self):
        for field in self.required_fields:
            if field not in self and self[field] is not None:
                raise NotImplementedError(f"Field {field} is required.")

    def __setitem__(self, key, value):
        if key in self.keys():
            raise ValueError(f"Value with key {key} already existed")
        super().__setitem__(key, value)
