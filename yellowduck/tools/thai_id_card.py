import re

class ThaiIDCardValidate():
    def __init__(self, nationality = 'th'):
        self.nationality = nationality

    def validate_id(self, id_card: str):
        result = -1
        if self.nationality == 'th':
            regexp = r"[0-9]+"
            id_card = ''.join(re.findall(regexp, id_card))
            if len(id_card) == 13:
                val = 0
                digit_pos = 13
                check_digit = id_card[-1]
                for digit in id_card[:-1]:
                    val = val + (int(digit) * digit_pos)
                    digit_pos = digit_pos - 1
                mod = val%11
                val = 11 - mod
                val = str(val)[-1]
                if val == check_digit:
                    result = id_card
        return result