import re


def remove_redundant_space(text: str) -> str:
    """
    Remove redundant space
    :param str text: text to be cleaned
    :return: clean text
    :rtype: str

    Example
    [In] text = 'หนาวมากก    ทำไมหนาวได้ขนาดนี้   Very cold     makk'
    [In] remove_redundant_space(text)
    [Out] 'หนาวมากก ทำไมหนาวได้ขนาดนี้ Very cold makk'
    """
    return " ".join(text.split())


def remove_http_https(text: str) -> str:
    text = re.sub(r"https\S+", " ", str(text))
    text = re.sub(r"http\S+", " ", str(text))
    return text


def remove_new_line(text: str) -> str:
    """
    Remove new line (\n)
    :param str text: text to be cleaned
    :return: clean text
    :rtype: str
    """
    text = str(text).replace("\n", " ")
    return text


def remove_tab_space(text: str) -> str:
    """
    Remove tab space (\t)
    :param str text: text to be cleaned
    :return: clean text
    :rtype: str
    """
    text = str(text).replace("\t", " ")
    return text


def remove_hashtag(text: str) -> str:
    """
    Remove hashtag
    """
    text = re.sub(r"#[A-Za-z0-9ก-๙]+", " ", str(text))
    return text


def remove_line_add(text: str) -> str:
    """
    Remove line@ id-liked form
    """
    text = re.sub(r"@[A-Za-z0-9ก-๙]+", " ", str(text))
    return text


def remove_punctuation(text: str, except_punct: list = []) -> str:
    """
    Remove punctuation
    """
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


def remove_emoji(text) -> str:
    """
    Remove emoji
    """
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
