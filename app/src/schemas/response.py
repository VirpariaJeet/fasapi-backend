from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


DataT = TypeVar('DataT')

class GenericResponse(GenericModel, Generic[DataT]):
    data: Optional[DataT] = Field(None)
    success: bool = Field(True)
    description: Optional[str] = Field(None)
    
    class Config:
        allow_population_by_field_name = True

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.update(exclude_none=True)
        return super().dict(*args, **kwargs)
