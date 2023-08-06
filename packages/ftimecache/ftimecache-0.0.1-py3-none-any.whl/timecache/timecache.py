# Copyright 2022 dimfred.1337@web.de
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import datetime as dt


def _make_safe(args):
    if isinstance(args, dict):
        res = []
        for k, v in args.items():
            res.append((k, _make_safe(v)))
        res = tuple(sorted(res))
    elif isinstance(args, (list, tuple, set)):
        res = (_make_safe(arg) for arg in args)
        res = tuple(sorted(res))
    else:
        res = args

    return res


def timecache(
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    milliseconds=0,
    microseconds=0,
    timedelta=None,
):
    cache = {}
    if timedelta is not None:
        refresh_after = timedelta
    else:
        refresh_after = dt.timedelta(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        )

    def deco(f):
        def wrap(*args, **kwargs):
            safe_args = [_make_safe(arg) for arg in args]
            safe_kwargs = list(_make_safe(kwargs))
            key = tuple(safe_args + safe_kwargs)

            if key not in cache:
                cache[key] = (dt.datetime(year=1970, month=1, day=1), None)
            time, res = cache[key]

            time_passed = dt.datetime.now() - time
            if time_passed > refresh_after:
                res = f(*args, **kwargs)
                cache[key] = dt.datetime.now(), res

            return res

        return wrap

    return deco
