import asyncio
import os

import click

from .CloudProject import CloudProject


from .._deploy import gcp

PATH = None

@click.group()
@click.option('--dir', default='.')
def cloudpost(dir):
    global PATH
    PATH = dir

@cloudpost.command()
@click.argument('name', type=str, default='')
def init(name: str):
    if name == '':
        name = os.path.basename(os.path.abspath(PATH))
    CloudProject.create_project(PATH, name)
    click.echo('Created project {}'.format(name))

def do_deployment(provider: str, proj: CloudProject):
    from cloudpost import depres
    depres._set_common_params(provider=provider)
    depres._set_common_params(project=proj)
    proj.collect()
    cur_state = {}
    def update_state(ent, status):
        # print(f' {status} {ent.type} {ent.name}')
        cur_state[ent] = status
        print('\x1b[H\x1b[J', end='')
        for n, v in cur_state.items():
            print(f' {v} {n.type} {n.name}')
    
    async def reader_function(ent):
        update_state(ent, '\x1b[36mRd\x1b[m')
        try:
            if hasattr(ent, 'read'):
                await ent.read()
            update_state(ent, '..')
        except:
            update_state(ent, '\x1b[31mEr\x1b[m')
            raise
    
    async def apply_function(ent):
        update_state(ent, '\x1b[36mWr\x1b[m')
        try:
            if hasattr(ent, 'apply'):
                await ent.apply()
            update_state(ent, '\x1b[32m✓✓\x1b[m')
        except:
            update_state(ent, '\x1b[31mEw\x1b[m')
            raise
            
    
    async def main():
        await depres.topological_invoke(lambda x: update_state(x, '--'))
        await depres.topological_invoke(reader_function)
        await depres.topological_invoke(apply_function)
    
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())


@cloudpost.command()
def deploy():
    proj = CloudProject(PATH)
    do_deployment(proj.get_provider(), proj)
    
@cloudpost.command()
def run():
    from .._deploy import local
    proj = CloudProject(PATH)
    local.initialize(proj)
    click.echo(' -- starting up local service --')
    do_deployment("local", proj)
    click.echo(' -- services started, running ---')
    local.start_listener()

@cloudpost.command()
def list():
    from cloudpost import depres
    from pprint import pprint
    proj = CloudProject(PATH)
    depres._set_common_params(provider=proj.get_provider())
    depres._set_common_params(project=proj)
    
    proj.collect()
    
    async def async_print(ent):
        print(ent.type, ent.name)
    
    # asyncio.run(depres.topological_invoke(async_print))
    
