from argparse import ArgumentParser
from os import makedirs
from os.path import abspath, dirname, exists, join

from typing import Any, Dict, Optional

__all__ = [
    'parse_console_arguments',
]


def parse_console_arguments(
    package: Optional[str] = None,
    subpath: Optional[str] = None,
) -> Dict[str, Any]:
    parser = ArgumentParser(
        description='Config files templater (Mako templates based).',
    )

    if package is None:
        parser.add_argument(
            '-p',
            '--package',
            required=True,
            help='Python package name.',
        )

    if subpath is None:
        parser.add_argument(
            '-s',
            '--subpath',
            required=False,
            default='config',
            help='Relative path inside selected python '
                 'package to directory with templates.',
        )

    parser.add_argument(
        '-t',
        '--type',
        required=False,
        help='Config template file type (deprecated).',
    )

    parser.add_argument(
        '-n',
        '--name',
        required=False,
        help='Config template file name.',
    )

    parser.add_argument(
        '-o',
        '--output',
        required=True,
        help='Destination config file (result) path.',
    )

    parser.add_argument(
        '--output-is-a-file',
        required=False,
        default=False,
        action='store_true',
        help='Will destination be a file?',
    )

    parser.add_argument(
        '--output-ext',
        required=False,
        default='ini',
        help='Destination config file extension (if it will '
             'be a file and directory declared as output).',
    )

    parser.add_argument(
        '--output-name',
        required=False,
        default=None,
        help='Destination config file name (if it will '
             'be a file and directory declared as output). '
             'It equals template name by default.',
    )

    parser.add_argument(
        'config_options',
        nargs='*',
        help='Config template variables.',
    )

    args = parser.parse_args()

    if not args.name and not args.type:
        parser.error('--name or --type option is required.')

    return {
        'config_options': dict(
            map(
                lambda opt: opt.split('=', 1), args.config_options,
            ),
        ),
        'package': getattr(args, 'package', None),
        'subpath': getattr(args, 'subpath', None),
        'template_name': args.name or args.type,
        'output_filepath': _get_output_path(
            args.output,
            args.output_ext,
            args.output_name or args.name or args.type,
            is_a_file=args.output_is_a_file,
        ),
    }


def _get_output_path(
    output: str,
    ext: str,
    name: str,
    is_a_file: bool = False,
) -> str:
    output = abspath(output)
    output_dir = dirname(output) if is_a_file else output

    if not exists(output_dir):
        makedirs(output_dir)

    if is_a_file:
        return output

    return join(output, f'{name}.{ext}')
