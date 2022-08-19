from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ResumeMatchedModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_resume: str = Field(...)
    job_index: int = Field(...)
    degree_matching: float = Field(...)
    major_matching: float = Field(...)
    skills_semantic_matching: float = Field(...)
    matching_score: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
