from typing import Dict, Type

from sqlalchemy.exc import StatementError


class UniqueConstraintFailed(StatementError):
    pass


error_mapping: Dict[str, Type[StatementError]] = {
    'duplicate entry': UniqueConstraintFailed
}
