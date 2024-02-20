from typing import Annotated

from pydantic import StringConstraints

NonBlankStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3)]
