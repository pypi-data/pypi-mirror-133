#!/usr/bin/env python3
import os
import sys
import time
import arrow
import shutil
from pathlib import Path
import json
import inquirer
import click
import subprocess
from . import cli
from .config import pass_config



@cli.command()
@pass_config
def list(config):
    pass


# dest_dir = os.path.expanduser(settings['dest_dir'])
# hosts = settings['hosts']
# data = hosts[which]
# if not data['path'].endswith('/'):
#     click.secho(f"Warning: {data['path']} does not end with '/' - does not work for symlinks.", fg='yellow')
# lines = subprocess.check_output([
#     "ssh",
#     "-oStrictHostKeyChecking=no",
#     data['host'],
#     "ls",
#     "-lhtra",
#     data['path'],
# ]).decode('utf-8').split("\n")
# orig_lines = lines
# if data.get('match', False):
#     match = " " + data['match']
#     lines = list(filter(lambda x: re.findall(match, x), lines))
#     dumpfile = re.findall(match, lines[-1])
#     dumpfile = dumpfile[0]
#     if ' ' in dumpfile:
#         dumpfile = dumpfile.split(" ")[-1]

# else:
#     lines = filter(lambda x: '{}.odoo'.format(which) in x and 'dump.gz' in x, lines)
#     if not lines:
#         lines = filter(lambda x: '{}'.format(which).lower() in x.lower() and 'dump' in x, orig_lines)
#     lines = list(lines)

#     lines = lines[-1]
#     lines = lines.split('\t')[-1]
#     lines = [x for x in lines.split("\n") if re.findall("{}.odoo.*.dump.gz".format(which), x)][0]
#     dumpfile = lines.split(" ")[-1]
# del lines
# click.echo(click.style("Found: {}".format(dumpfile), bold=True))
# dest_path = dest_dir.format(hosts[which].get('transform_name', which))
# print("RSyncing to {}".format(dest_path))
# proc = subprocess.Popen([
#     "rsync",
#     '{}:{}/{}'.format(data['host'], data['path'], dumpfile),
#     dest_path,
#     '-arP'
# ])
# proc.wait()

# stat = os.stat(dest_path)
# click.echo("\n\nFile size is: {}".format(humanize.naturalsize(stat.st_size)))

# md5sum = subprocess.check_output([
#     "ssh",
#     "-oStrictHostKeyChecking=no",
#     data['host'],
#     "md5sum",
#     '{}/{}'.format(data['path'], dumpfile),
# ]).decode('utf-8')
# print("\n\n")
# print("Source MD5:\t\t\t  {}".format(md5sum.split(" ")[0]))
# os.system("md5 {}".format(dest_path))
