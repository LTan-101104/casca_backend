from sqlalchemy.orm import Mapped, mapped_column

from .base import CreatedUpdatedAtMixin


class SampleModel(CreatedUpdatedAtMixin): #just a sample model to put in our controller
    __tablename__ = "samples"
    id: Mapped[int] = mapped_column(primary_key=True)
