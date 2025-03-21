from typing import Generic, TypeVar

from sqlalchemy.orm.session import Session

from app.models import BaseModel
#This is more like service, controller is where you map route to the service

Model = TypeVar("Model", bound=BaseModel)


class Controller(Generic[Model]):

    def __init__(self, session: Session):
        self.session = session
        self.model: type[Model] = type(Model)

    # some base operations
    # Note: controller needs to also provide de(serialization),
    # or it can be imported from the separate layer
    def get(self, pk: int) -> Model:
        return self.session.get(self.model, pk)
