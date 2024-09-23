import re
import string

import pandas as pd
import pythainlp
from preda.logger import logger
from preda.nlp import utils as nutils
from tqdm import tqdm


def execute(item_names: pd.Series) -> pd.Series:
    """Process item names by cleaning and normalizing text.

    Args:
        item_names (pd.Series): A pandas Series containing item names to be processed.

    Returns:
        pd.Series: A pandas Series containing the processed item names.
    """
    tqdm.pandas()

    processed_item_names = item_names.astype("string").progress_apply(
        nutils.remove_new_line
    )
    processed_item_names = processed_item_names.progress_apply(nutils.remove_tab_space)
    processed_item_names = processed_item_names.progress_apply(nutils.remove_http_https)
    # processed_item_names = processed_item_names.progress_apply(remove_phone_number)
    processed_item_names = remove_phone_number(processed_item_names)
    processed_item_names = processed_item_names.str.lower()
    processed_item_names = processed_item_names.progress_apply(pythainlp.util.normalize)
    processed_item_names = processed_item_names.progress_apply(nutils.remove_emoji)
    # processed_item_names = processed_item_names.progress_apply(remove_digit)
    processed_item_names = remove_digit(processed_item_names)
    processed_item_names = processed_item_names.progress_apply(nutils.replace_rep_after)
    # processed_item_names = processed_item_names.progress_apply(
    #     efficiently_remove_punctuation
    # )
    processed_item_names = efficiently_remove_punctuation(processed_item_names)
    processed_item_names = processed_item_names.progress_apply(
        nutils.remove_useless_spaces
    )
    processed_item_names = processed_item_names.str.strip()
    # processed_item_names = processed_item_names.progress_apply(add_space_between_th_en)
    processed_item_names = add_space_between_th_en(processed_item_names)

    diff_text_cond = processed_item_names != item_names
    logger.info(f"There are {sum(diff_text_cond)} processed item names.")
    import pdb

    pdb.set_trace()
    return processed_item_names


def with_progress(func_name):
    def decorator(func):
        def wrapper(series, *args, **kwargs):
            # Set the description for the progress bar
            tqdm.pandas(desc=func_name)
            result = series.progress_apply(func, *args, **kwargs)

            # Clear the description after the operation
            tqdm.pandas(desc=False)
            return result

        return wrapper

    return decorator


###


@with_progress("remove_phone_number")
def remove_phone_number(text: str) -> str:
    """Removes phone numbers from the input text.

    This function uses a regular expression to identify and remove phone numbers from the input text. The pattern matches common Thai phone number formats.

    Args:
        text (str): The input text from which phone numbers will be removed.

    Returns:
        str: The text with phone numbers removed.
    """
    phone_number_pattern = re.compile(r"\b(0[689]{1}[\d]{1}-?)+([\d]{3}-?)+([\d]{4})\b")
    return phone_number_pattern.sub("", text)


###


@with_progress("remove_digit")
def remove_digit(text: str) -> str:
    """Remove digits from the input text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with digits removed.
    """
    digit_pattern = re.compile(r"[๐-๙0-9]")
    return digit_pattern.sub("", text)


###


@with_progress("efficiently_remove_punctuation")
def efficiently_remove_punctuation(text: str) -> str:
    """Remove punctuation from the input text.

    This function uses a regular expression to identify and remove punctuation from the input text.

    Args:
        text (str): The input text from which punctuation will be removed.

    Returns:
        str: The text with punctuation removed.
    """
    return my_punctuation_pattern.sub(" ", text)


# Compile the base punctuation regex pattern only once
_base_punctuation_list = set(re.escape(p) for p in string.punctuation)


def process_punctuation_pattern(
    punctuation_list: list[str] = [],
    exceptional_punc_list: list[str] = [],
    overwrite: bool = False,
) -> re.Pattern:
    """Create a regex pattern for punctuation characters, considering exceptional cases.

    Args:
        punctuation_list (List[str]): List of punctuation characters to include.
        exceptional_punc_list (List[str]): List of punctuation characters to exclude.
        overwrite (bool): Whether to overwrite the base punctuation list.

    Returns:
        re.Pattern: Compiled regex pattern for punctuation characters.
    """

    # Combine base punctuations with custom ones, handling exceptions
    if overwrite:
        punctuations = set(re.escape(p) for p in punctuation_list)
    else:
        punctuations = _base_punctuation_list.union(
            re.escape(p) for p in punctuation_list
        )

    # Remove any exceptional punctuation from the final set
    punctuations -= set(re.escape(p) for p in exceptional_punc_list)

    # Compile and return the regex pattern
    return re.compile(f"[{''.join(punctuations)}]+")


# Example custom punctuation list and pattern precompilation
my_punctuation_list = [
    "#",
    "@",
    "/",
    ".",
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
    "%",
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

# Precompile the punctuation pattern once, avoiding repeated recomputation
my_punctuation_pattern = process_punctuation_pattern(my_punctuation_list)


###


@with_progress("add_space_between_th_en")
def add_space_between_th_en(text: str) -> str:
    # Add space between Thai and English characters
    spaced_text_pattern = re.compile(r"([ก-๙])([a-zA-Z])|([a-zA-Z])([ก-๙])")
    return spaced_text_pattern.sub(r"\1 \2", text)
