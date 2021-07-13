from marshmallow import ValidationError


class DeserializationMixin:
    def deserialize(self, json: dict):
        instance = None
        try:
            instance = self.load(json)
        except ValidationError as err:
            print({"message": str(err)})
        return instance
