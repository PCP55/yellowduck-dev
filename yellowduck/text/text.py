"""Text cleansing function which are used very frequently.

Usage:

```
from yellowduck.preprocessing.text import TextCleansing

Using all function
text = yellowduck.preprocessing.text.TextCleansing.pipeline(my_text)

-Individual-
text = TextCleansing.http_https(text)
text = TextCleansing.new_line(text)
text = TextCleansing.tab_space(text)
text = TextCleansing.hashtag(text)
text = TextCleansing.punctuation(text)
text = TextCleansing.emoji(text)
text = TextCleansing.redundant_space(text)
```
Arguments:
    text: python string.
Returns:
    A python string.
"""

import re


class TextCleansing:
    def http_https(text: str) -> str:
        text = re.sub(r"https\S+", "", str(text))
        text = re.sub(r"http\S+", "", str(text))
        return text

    # Remove new line (\n) and tab space (\t)
    def new_line(text: str) -> str:
        text = str(text).replace("\n", " ")
        return text

    def tab_space(text: str) -> str:
        text = str(text).replace("\t", " ")
        return text

    # Remove hashtag and line@ id
    def hashtag(text: str) -> str:
        text = re.sub(r"#[A-Za-z0-9ก-๙]+", " ", str(text))
        text = re.sub(r"@[A-Za-z0-9ก-๙]+", " ", str(text))
        return text

    # Clean Symbol
    def punctuation(text: str, except_punct: list = []) -> str:
        puncts = [
            ",",
            '"',
            ":",
            ")",
            "(",
            "-",
            "!",
            "?",
            "|",
            ";",
            "'",
            "$",
            "&",
            "[",
            "]",
            ">",
            "%",
            "=",
            "#",
            "*",
            "+",
            "\\",
            "•",
            "~",
            "@",
            "£",
            "·",
            "_",
            "{",
            "}",
            "©",
            "^",
            "®",
            "`",
            "<",
            "→",
            "°",
            "€",
            "™",
            "›",
            "♥",
            "←",
            "×",
            "§",
            "″",
            "′",
            "Â",
            "█",
            "½",
            "à",
            "…",
            "\xa0",
            "\t",
            "“",
            "★",
            "”",
            "–",
            "●",
            "â",
            "►",
            "−",
            "¢",
            "²",
            "¬",
            "░",
            "¶",
            "↑",
            "±",
            "¿",
            "▾",
            "═",
            "¦",
            "║",
            "―",
            "¥",
            "▓",
            "—",
            "‹",
            "─",
            "\u3000",
            "\u202f",
            "▒",
            "：",
            "¼",
            "⊕",
            "▼",
            "▪",
            "†",
            "■",
            "’",
            "▀",
            "¨",
            "▄",
            "♫",
            "☆",
            "é",
            "¯",
            "♦",
            "¤",
            "▲",
            "è",
            "¸",
            "¾",
            "Ã",
            "⋅",
            "‘",
            "∞",
            "«",
            "∙",
            "）",
            "↓",
            "、",
            "│",
            "（",
            "»",
            "，",
            "♪",
            "╩",
            "╚",
            "³",
            "・",
            "╦",
            "╣",
            "╔",
            "╗",
            "▬",
            "❤",
            "ï",
            "Ø",
            "¹",
            "≤",
            "‡",
            "√",
            "•",
            "!",
        ]

        for punct in puncts:
            text = text.replace(punct, " ")
        return text

    # Remove emoji
    def emoji(text) -> str:
        emoj = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+",
            re.UNICODE,
        )
        return re.sub(emoj, " ", text)

    def redundant_space(text) -> str:
        return " ".join(text.split())
