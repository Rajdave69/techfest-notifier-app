import click
from commands import reminder, notification


@click.group()
def entry_point():
    pass


entry_point.add_command(reminder)
entry_point.add_command(notification)
if __name__ == "__main__":
    entry_point()
