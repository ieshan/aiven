import importlib
import os

import click


class ManageCLI(click.MultiCommand):
	def list_commands(self, ctx):
		command_list = []
		for filename in os.listdir("commands"):
			if filename.endswith(".py") and filename != "__init__.py":
				command_list.append(filename[:-3])
		command_list.sort()
		return command_list

	def get_command(self, ctx, name):
		if name == "__init__":
			return None

		cmd = importlib.import_module("commands." + name).command

		if not isinstance(cmd, click.Command):
			return None
		return cmd


cli = ManageCLI(help="manage.py help text")


if __name__ == "__main__":
	cli()
