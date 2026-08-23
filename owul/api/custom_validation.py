import jsonschema
from flask_restx import fields
import datetime

custom_checker = jsonschema.FormatChecker()


def format_validation(cls):
    def wrapper(*args, **kwargs):
        custom_checker.checks(cls.__schema_format__, ValueError)(cls.validate)
        return cls
    
    return wrapper


@format_validation
class Time(fields.String):
    __schema_format__ = "time"

    def validate(value: str):
        value = str(value)
        if ":" not in value:
            raise ValueError

        hours_str, minutes_str = value.split(":", maxsplit=1)

        hours, minutes = int(hours_str), int(minutes_str)
        if hours > 24 or hours < 0:
            raise ValueError
        
        if minutes > 60 or minutes < 0:
            raise ValueError

        if f"{hours:0>2}" != hours_str:
            raise ValueError
        
        if f"{minutes:0>2}" != minutes_str:
            raise ValueError

        return True


@format_validation
class DateTime(fields.String):
    __schema_format__ = "datetime"

    def validate(value: str):
        value = str(value)
        dt = datetime.datetime.fromisoformat(value)
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            raise ValueError
        
        return True