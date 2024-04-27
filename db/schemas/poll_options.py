from enum import StrEnum, auto


class PollOptions(StrEnum):
    AGREE = "من موافقم"
    DISAGREE = "من مخالفم"
    NONE = auto()

    @classmethod
    def agree_index(cls):
        return cls.as_list().index(PollOptions.AGREE)

    @classmethod
    def disagree_index(cls):
        return cls.as_list().index(PollOptions.DISAGREE)

    @classmethod
    def none_index(cls):
        return -1

    @classmethod
    def as_list(cls):
        return [PollOptions.AGREE, PollOptions.DISAGREE]
