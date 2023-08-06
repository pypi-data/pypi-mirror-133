# timecache

Decorator to cache function return values based on time.

## Install

    pip3 install ftimecache

## Usage

    from ftimecache import ftimecache

    @ftimecache(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7)
    def your_function(*args, **kwargs):
        # do something

    # OR
    from datetime import timedelta

    @ftimecache(timedelta=timedelta(weeks=1, ...))
    def your_function(*args, **kwargs):
        # do something
