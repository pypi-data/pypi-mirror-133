import click

from .lambdaOpts import install, publish


@click.command(name='publish', help='Publish lambda')
def lambda_publish():
    publish()


@click.command(name='install', help='Install lambda')
@click.argument('name', required=True, type=str)
def lambda_install(name):
    install(name)


@click.group(name='lambda', help='Lambda commands')
def lambda_ns():
    pass


lambda_ns.add_command(lambda_publish)
lambda_ns.add_command(lambda_install)


@click.command(name='login', help='Login commands')
def login_ns():
    click.echo('login')


@click.group()
def start():
    pass


start.add_command(lambda_ns)
start.add_command(login_ns)


if __name__ == '__main__':
    start()
