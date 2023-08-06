# -*- coding: utf-8 -*-

import click

from .base import activity, get_target_time


@click.command()
@click.option('--t', default=10, help="seconds to wait before repeating the action.")
@click.option('--stoptime', help="A time in iso format (e.g., 08:30) to stop running.")
def main(t, stoptime):
    if stoptime is not None:
        stoptime = get_target_time(stoptime)
    activity(sleep_time=t, stop_time=stoptime)
    exit(0)


if __name__ == "__main__":
    main()
