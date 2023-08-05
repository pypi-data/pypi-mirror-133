from typing import Any, TypeVar, Dict, Union

from sqlalchemy.orm.attributes import History


class Change:
    """ Simplified `History` Structure

    """
    previous_value: Any
    current_value: Any

    def __init__(self, history: History):
        changed = history.has_changes()
        self.changed = changed

        if not changed:
            return

        self.previous_value = history.deleted[0]
        self.current_value = history.added[0]


Changes = Dict[str, Change]