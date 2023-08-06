from pydantic import BaseModel


class BaseDataModel(BaseModel):
    def dict(self, **kwargs):
        hidden_fields = [field for field in list(self.__fields__.keys()) if field[0] == '_']
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)
