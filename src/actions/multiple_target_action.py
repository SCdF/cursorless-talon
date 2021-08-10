from ..primitive_target import STRICT_HERE
from talon import Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.cursorless
"""


mod.list("cursorless_multiple_target_action", desc="Cursorless move or bring actions")
ctx.lists["self.cursorless_multiple_target_action"] = {"bring", "move", "swap", "call"}


mod.list(
    "cursorless_target_separator", desc="A symbol that comes in pairs, eg brackets"
)
ctx.lists["self.cursorless_target_separator"] = {
    "at",
    "before",
    "after",
}


@mod.capture(
    rule=(
        "[{user.cursorless_target_separator}] <user.cursorless_target> | "
        "<user.cursorless_target> {user.cursorless_target_separator} <user.cursorless_target>"
    )
)
def cursorless_multiple_targets(m) -> str:
    target_list = m.cursorless_target_list

    try:
        target_separater = m.cursorless_target_separator
        if target_separater != "at":
            target_list[-1]["position"] = target_separater
    except AttributeError:
        target_separater = None

    if len(target_list) == 1:
        if target_separater is not None:
            target_list = [STRICT_HERE] + target_list
        else:
            target_list = target_list + [STRICT_HERE]

    return target_list
