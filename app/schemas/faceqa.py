from pydantic import BaseModel


class FaceQARequest(BaseModel):
    pass


class FaceQAResponse(BaseModel):
    quality_score: float
