import click
import sys
from pathlib import Path
from .config import pass_config
import inquirer
from .default_command import DefaultCommandGroup
from click import CompletionItem

global_data = {
    'config': None
}

class SourceVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        choices = config.settings['hosts'].keys()
        return [
            CompletionItem(x)
            for x in choices
        ]

@click.group(invoke_without_command=True, cls=DefaultCommandGroup)
@click.option('-s', '--source', required=True)
@pass_config
def cli(config, source):
    global_data['config'] = config



from . import fetch_latest_dump