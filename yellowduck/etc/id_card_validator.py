from abc import ABC, abstractmethod
import re


class IDCardStrategy(ABC):
    @abstractmethod
    def is_valid(self, **kwargs):
        pass


class NationalThaiIDCard(IDCardStrategy):
    def is_valid(self, id: str, **kwargs) -> bool:
        regexp = r"[0-9]+"
        id = "".join(re.findall(regexp, id))
        if len(id) == 13:
            val = 0
            digit_pos = 13
            check_digit = id[-1]
            for digit in id[:-1]:
                val = val + (int(digit) * digit_pos)
                digit_pos = digit_pos - 1
            mod = val % 11
            val = 11 - mod
            val = str(val)[-1]
            return str(val) == str(check_digit)
        else:
            raise ValueError("Invalid ID")


class IDValidator:
    def __init__(
        self, id: str = id, id_type: IDCardStrategy = NationalThaiIDCard(), **kwargs
    ):
        self.id = id
        self.id_type = id_type
        self.id_type_extras = kwargs.get("id_type_extras", {})

    def validate(self):
        return self.id_type.is_valid(id=self.id)
