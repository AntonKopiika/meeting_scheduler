from marshmallow import Schema, ValidationError, fields, post_load


class Request:
    def __init__(self, user, start, end):
        self.user = user
        self.start = start
        self.end = end

    def __repr__(self):
        return f'<Request: user_id={self.user} ' \
               f'from {self.start} to {self.end}>'


class RequestSchema(Schema):
    user = fields.Int()
    start = fields.Date()
    end = fields.Date()

    @post_load
    def make_request(self, data, **kwargs):
        return Request(**data)

    def get_request(self, data):
        req = None
        try:
            req = self.load(data)
        except ValidationError as err:
            # TODO: make logging error
            print({"message": str(err)})
        return req
