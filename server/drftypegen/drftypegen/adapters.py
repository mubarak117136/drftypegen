import logging

from collections import OrderedDict
from rest_framework.fields import *
from rest_framework import serializers as r_s
from wagtail.core import fields as wg_fields
from django.db import models as dj_model

logger = logging.getLogger(__name__)

DRF_COMPOSITE_FIELDS = ["ListSerializer", "ManyRelatedField"]

DRF_LIST_FIELDS = ["ListSerializer", "ManyRelatedField"]

DRF_COMPOSITE_FIELD_RELATION_NAMES = {"ListSerializer": "child", "ManyRelatedField": "child_relation"}

WAGTAIL_COMPOSITE_FIELDS = ["StreamField", ]

DRF_FIELDS = {
        BooleanField: "boolean",
        NullBooleanField: "boolean",

        CharField: "string",
        EmailField: "string",
        RegexField: "string",
        SlugField: "string",
        URLField: "string",
        UUIDField: "string",
        FilePathField: "string",
        IPAddressField: "string",

        IntegerField: "integer",
        FloatField: "number",
        DecimalField: "number",

        DateTimeField: "string",
        DateField: "string",
        TimeField: "string",
        DurationField: "string",

        ChoiceField: "string",
        MultipleChoiceField: "string",

        FileField: "string",
        ImageField: "string",

        ListField: "list",
        DictField: "dict",

        JSONField: "json",

        r_s.PrimaryKeyRelatedField: "integer",
        r_s.ManyRelatedField: "list"
    }


WAGTAIL_FIELDS = {
    dj_model.CharField: "string",
    wg_fields.RichTextField: "string",
    dj_model.ForeignKey: "integer",
    wg_fields.StreamField: "child"
}

class BaseAdapter:
    def __init__(self, serializer):
        self.serializer = serializer
        self.instance = serializer()

    def transform_field(self, field):
        return {
            "read_only": False,
            "write_only": False,
            "required": True,
        }

    def get_serializer_fields(self):
        return OrderedDict([])

    def get_transformed_data(self):
        fields = self.get_serializer_fields()
        nested = []
        data = OrderedDict([])

        for field in fields.items():
            #logger.critical(field[0])
            #logger.critical(field[1])
            #logger.critical("=====")
            field_data = self.transform_field(field)
            data[field[0]] = field_data[0]
            nested += field_data[1]
        if hasattr(self.serializer.Meta, 'model'):
            name = self.serializer.Meta.model.__name__
        else:
            name = self.serializer.__name__
        nested.append({
            'name': name,
            'fields': data
        })
        return nested


class SerializerAdapter(BaseAdapter):
    def get_serializer_fields(self):
        return self.instance.get_fields()

    def transform_field(self, field):
        nested = []
        data = {
            'name': field[0],
            'read_only': field[1].read_only,
            'write_only': field[1].write_only,
            'required': field[1].required,
            'nullable': field[1].allow_null,
        }
        field_class = field[1].__class__
        type_data = DRF_FIELDS.get(field_class, None)
        data['openapi_type'] = type_data
        data['type'] = field_class.__name__
        if data['type'] in DRF_COMPOSITE_FIELDS:
            child_class = getattr(field[1], DRF_COMPOSITE_FIELD_RELATION_NAMES[data["type"]]).__class__
            if child_class.__name__ == "PrimaryKeyRelatedField":
                data['child'] = 'number'
            else:
                nested_data = SerializerAdapter(child_class).get_transformed_data()
                data['child'] = nested_data[0]["name"]
                nested.extend(nested_data)
        return data, nested

from pprint import pprint

class WagtailAdapter:
    def __init__(self, wagtail_model):
        self.wagtail_model = wagtail_model

    def get_all_fields(self):
        return self.wagtail_model.api_fields

    def get_transformed_data(self):
        fields = self.get_all_fields()
        data = OrderedDict([])
        nested = []

        for field in fields:
            field = getattr(self.wagtail_model, field.name).field
            field_data = self.transform_field(field)
            data[field.name] = field_data

        nested.append({
            'name': self.wagtail_model.__name__,
            'fields': data
        })
        return nested

    def stream_field_parser(self, stream_field):
        list_block = [block for block in stream_field.stream_block.child_blocks.items()]
        for block in list_block:
            block_name = block[0]
            blocks = block[1]
            child_block = blocks.child_blocks
            for child in child_block.items():
                if child[1].__class__.__name__ == 'ListBlock':
                    pprint(vars(child[1].child_block))


    def transform_field(self, field):
        data = {
            'name': field.name,
            'null': field.null,
            'blank': field.blank
        }
        field_class = field.__class__
        type_data = WAGTAIL_FIELDS.get(field_class, None)
        data['openapi_type'] = type_data
        data['type'] = field_class.__name__

        if data['type'] in WAGTAIL_COMPOSITE_FIELDS:
            self.stream_field_parser(field)
        return data
