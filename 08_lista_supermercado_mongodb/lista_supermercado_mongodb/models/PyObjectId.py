"""Modelos usados para a criação das tabelas no banco de dados"""

# Bibliotecas
from pydantic import BaseModel, Field as PydanticField
from bson import ObjectId

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from typing import Any, Dict

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):

            raise ValueError("Invalid objectid")

        return ObjectId(v)

#    @classmethod
#    def __modify_schema__(cls, field_schema):
#        field_schema.update(type="string")
        
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples='examples')
        return json_schema    
