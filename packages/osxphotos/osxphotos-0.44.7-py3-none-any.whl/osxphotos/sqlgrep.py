"""Search through a sqlite database file for a given string"""

import sqlite3
from typing import Callable, Optional
import re
from rich import print as rprint


def sqlgrep(
    filename: str,
    pattern: str,
    ignore_case: bool = False,
    print_filename: bool = True,
) -> None:
    flags = re.IGNORECASE if ignore_case else 0
    try:
        with sqlite3.connect(f"file:{filename}?mode=ro", uri=True) as conn:
            regex = re.compile(r"(" + pattern + r")", flags=flags)
            filename_header = f"{filename}: " if print_filename else ""
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            for tablerow in cursor.fetchall():
                table = tablerow[0]
                cursor.execute("SELECT * FROM {t}".format(t=table))
                for row_num, row in enumerate(cursor):
                    for field in row.keys():
                        field_value = row[field]
                        if not field_value or type(field_value) == bytes:
                            # don't search binary blobs
                            next
                        field_value = str(field_value)
                        if re.search(pattern, field_value, flags=flags):
                            row_str = regex.sub(r"[bold]\1[/bold]", field_value)
                            rprint(
                                f"{filename_header}{table}, {field}, {row_num}, {row_str}"
                            )
    except sqlite3.DatabaseError as e:
        raise sqlite3.DatabaseError(f"{filename}: {e}")