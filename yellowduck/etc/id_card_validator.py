from abc import ABC, abstractmethod
import re


class IDCardStrategy(ABC):
    @abstractmethod
    def is_valid(self, **kwargs):
        pass


class NationalThaiIDCard(IDCardStrategy):
    """
    Thai National ID Card Validation

    Reference:
    https://adamblog.co/google-sheet-thai-id-checker-function/#:~:text=%E0%B8%95%E0%B8%B1%E0%B8%A7%E0%B9%80%E0%B8%A5%E0%B8%82%E0%B8%9A%E0%B8%99%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%A3%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%8A%E0%B8%B2%E0%B8%8A%E0%B8%99%E0%B8%A1%E0%B8%B5,%E0%B8%95%E0%B8%A3%E0%B8%87%E0%B8%81%E0%B8%B1%E0%B8%99%E0%B9%81%E0%B8%AA%E0%B8%94%E0%B8%87%E0%B8%A7%E0%B9%88%E0%B8%B2%E0%B8%96%E0%B8%B9%E0%B8%81%E0%B8%95%E0%B9%89%E0%B8%AD%E0%B8%87
    """

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
    """
    IDValidator - Check whether id is valid or not
    :param str id: id to be checked
    :param str id_type:  type of id needed
    :return: True as valid id and False as invalid id
    :rtype: boolean
    """

    def __init__(
        self, id: str = id, id_type: IDCardStrategy = NationalThaiIDCard(), **kwargs
    ):
        self.id = id
        self.id_type = id_type
        self.id_type_extras = kwargs.get("id_type_extras", {})

    def validate(self):
        return self.id_type.is_valid(id=self.id)
