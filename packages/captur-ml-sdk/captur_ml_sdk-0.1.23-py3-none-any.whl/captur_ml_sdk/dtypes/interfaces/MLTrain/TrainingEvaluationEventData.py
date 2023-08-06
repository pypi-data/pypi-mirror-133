from pydantic import BaseModel


class TrainingEvaluationEventData(BaseModel):
    model_id: str
