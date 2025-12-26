from argparse import _SubParsersAction, ArgumentParser


def handle_install(args):
    version = args.version
    install_dir = args.dir
    write_path = args.write_path
    
    print(f"Installing Python {version}")
    if install_dir:
        print(f"Install directory: {install_dir}")
    if write_path:
        print("Will write to user PATH")
    
    # TODO: Implement installation logic


def install_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'install',
        help='Install a specific Python version'
    )

    parser.add_argument(
        'version',
        help='Python version to install (e.g., 3.11.0)'
    )

    parser.add_argument(
        '--dir',
        help='Installation directory',
        default=None
    )

    parser.add_argument(
        '--write-path',
        action='store_true',
        help='Write the install binaries to user PATH'
    )

    parser.set_defaults(func=handle_install)

    