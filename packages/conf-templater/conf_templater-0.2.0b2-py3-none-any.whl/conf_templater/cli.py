from typing import Any, Optional

from .console import parse_console_arguments
from .template import render_template

__all__ = [
    'run_config_templating',
]


def run_config_templating(
    package: Optional[str] = None,
    subpath: Optional[str] = None,
    **render_options: Any,
) -> None:
    args = parse_console_arguments(package=package, subpath=subpath)
    render_template(
        package if package is not None else args['package'],
        subpath if subpath is not None else args['subpath'],
        args['template_name'],
        args['output_filepath'],
        args['config_options'],
        **render_options,
    )


if __name__ == '__main__':
    run_config_templating()
