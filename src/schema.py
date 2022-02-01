from marshmallow import Schema, fields


class WarnNoticeSchema(Schema):
    """An standardized instance of a WARN Act Notice."""

    state = fields.Str(max_length=2, required=True)
    company = fields.Str(required=True)
    date = fields.Date(required=True)
    jobs = fields.Int(required=True)
