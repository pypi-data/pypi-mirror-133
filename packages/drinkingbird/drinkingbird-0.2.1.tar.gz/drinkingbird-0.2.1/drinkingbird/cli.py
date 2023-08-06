# -*- coding: utf-8 -*-

import click

from .base import activity, get_target_time
from .actions import action_descriptions
from .art import Printer


@click.command()
@click.option('--t', default=10, help="seconds to wait before repeating the action.")
@click.option('--action', type=click.Choice(action_descriptions), default="control-tab",
              help="Action to perform. Options are: %s." % "; ".join("%s: %s" % a for a in action_descriptions.items()))
@click.option('--stoptime', help="A time in iso format (e.g., 08:30) to stop running.")
@click.option('--anim/--no-anim', default=True, help="Show an animation in the console")
def main(t, stoptime, anim, action):
    if stoptime is not None:
        stoptime = get_target_time(stoptime)

    if anim:
        monitor = Printer()
        monitor()  # First output
    else:
        monitor = None

    activity(sleep_time=t, stop_time=stoptime, action=action, monitor=monitor)
    exit(0)


if __name__ == "__main__":
    main()
