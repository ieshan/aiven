import click


@click.command(name="command1")
def command():
	click.echo("command 1")
