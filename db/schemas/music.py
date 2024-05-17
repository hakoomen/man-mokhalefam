from pydantic import BaseModel, ConfigDict, model_validator


class Base(BaseModel):
    chat_id: str
    audio_name: str

    @model_validator(mode="after")
    def strip_and_lower_audio_name(self):
        self.audio_name = self.audio_name.strip().lower()
        return self


class MusicRead(Base):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MusicCreate(Base):
    pass
