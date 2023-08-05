import os
import click
from mmflyer import __version__


class Environment:
    """Context class holding state for cli commands"""
    def __init__(self):
        self.cwd = os.getcwd()
        self.part_count = 0
        self.assembly_count = 0
        self.model_path = "tests/test_data"
        self.model_name = "model"
        self.debug = False

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))

class CLI(click.MultiCommand):
    """Modular CLI class"""
    def list_commands(self, ctx):
        """scan command directory and list all cli commands"""
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """import cli command file on demand"""
        try:
            mod = __import__(f"mmdesigner.commands.cmd_{name}", None, None, ["cli"])
        except ImportError: # pragma: no cover
            return
        return mod.cli

@click.version_option(__version__, "-v", "--version")

@click.command(cls=CLI)
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.option("--model_path", help="Path to model directory")
@click.option("--model_name", help="Name of model within model_path")
@pass_environment
def cli(ctx, debug, model_path, model_name):
    """primary CLI interface"""
    ctx.debug = debug
    if not model_path is None:
        ctx.model_path = model_path
    if not model_name is None:
        ctx.model_name = model_name
