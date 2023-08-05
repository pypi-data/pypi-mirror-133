# This file stores global information that the framework accesses
# Most of this stuff is accessed to allow for logic that makes
# The developer's life easier
# fgloblas = frameworkglobals
# globals is a python keyword, so we avoid shadowing it

from typing import Optional

from starlette.templating import Jinja2Templates


templates_directory: str = "templates/"
templating_engine: Jinja2Templates = Jinja2Templates(directory=templates_directory)


# methods to help internally with updating globals

def _update_templating_engine(directory: Optional[str] = None) -> Jinja2Templates:
    engine = Jinja2Templates(directory=(directory or templates_directory))
    return engine # incase somewhere we need to use the new engine