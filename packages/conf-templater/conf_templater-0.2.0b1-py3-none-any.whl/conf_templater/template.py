import os
from typing import Any, Mapping

from mako.template import Template
from pkg_resources import resource_filename

from .exc import ConfigTemplaterFileNotFoundError, ConfigTemplaterPackageError

__all__ = [
    'render_template',
]

_DEFAULT_RENDER_OPTIONS = {
    'input_encoding': 'utf-8',
    'output_encoding': 'utf-8',
    'strict_undefined': True,
}


def render_template(
    package: str,
    subpath: str,
    template_name: str,
    output_filepath: str,
    config_data: Mapping[str, Any],
    **render_options: Any,
) -> None:
    try:
        template_root = resource_filename(
            package, subpath,
        )
    except ImportError as err:
        raise ConfigTemplaterPackageError() from err

    template_render_options = _DEFAULT_RENDER_OPTIONS.copy()
    template_render_options.update(render_options)

    template_filepath = os.path.join(
        template_root, f'{template_name}.mako',
    )

    try:
        template = Template(
            filename=template_filepath,
            **template_render_options,
        )
    except FileNotFoundError as err:
        raise ConfigTemplaterFileNotFoundError() from err

    with open(output_filepath, 'wb') as file:
        try:
            file.write(template.render(**config_data))
        except NameError as err:
            print(f'Не указан параметр для шаблона. {err!r}.')
