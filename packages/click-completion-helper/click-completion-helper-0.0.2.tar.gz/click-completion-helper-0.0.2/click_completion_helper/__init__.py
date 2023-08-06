import click
import subprocess
import os
import sys
from pathlib import Path
import shellingham

import inspect
import os
from pathlib import Path
current_dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

@click.group()
def cli():
    pass

@cli.command(help="Name of the console call.")
@click.argument("name")
def setup(name):
    def setup_for_shell_generic(shell):
        path = Path(f"/etc/{shell}_completion.d")
        NAME = name.upper().replace("-", "_")
        cmd = subprocess.check_output(["which", name]).strip().decode('utf-8')
        env = os.environ.copy()
        if not cmd:
            click.secho(f"Could not find command: {name}")
            sys.exit(-1)
        env[f"_{NAME}_COMPLETE"] = "source_" + shell
        try:
            completion = subprocess.check_output(cmd, env=env)
        except subprocess.CalledProcessError as ex:
            completion = ex.output
        if path.exists():
            if os.access(path, os.W_OK):
                (path / name).write_bytes(completion)
                return

        if not (path / name).exists():
            rc = Path(os.path.expanduser("~")) / f'.{shell}rc'
            if not rc.exists():
                return
            complete_file = rc.parent / f'.{name}-completion.sh'
            complete_file.write_bytes(completion)
            if complete_file.name not in rc.read_text():
                content = rc.read_text()
                content += '\nsource ~/' + complete_file.name
                rc.write_text(content)

    setup_for_shell_generic(shellingham.detect_shell()[0])