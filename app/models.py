from pydantic import BaseModel, HttpUrl

class Vacancy(BaseModel):
    title: str
    url: HttpUrl
    salary: str