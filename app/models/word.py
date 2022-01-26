from bson import ObjectId
from pydantic import Field, BaseModel


from app.models.models import PyObjectId


class WordModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    russian_name: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "russian": "Привет",
            }
        }


class UpdateWordModel(BaseModel):
    russian: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "russian": "Привет"
            }
        }