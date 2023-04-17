from argparse import ArgumentParser
from datetime import datetime

import pytz


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Allows to compute a list of possible locations by"
        "user's local time by comparing it to knows offsets",
    )
    parser.add_argument(
        "local_time",
        help="Local time. Specify --offset parameter with the UTC offset corresponding to this time. If the offset is not known, specify --unknown-offset",
        type=datetime.fromisoformat,
    )
    parser.add_argument(
        "utc_time",
        help="UTC time at the same moment",
        type=datetime.fromisoformat,
    )
    parser.add_argument(
        "--allowed-delta",
        help="Allowed difference, in minutes, between the localized time and the actual time. "
        "Please allow for at least 2 min differences",
        default=5,
        type=float,
    )
    args = parser.parse_args()

    utc_time = args.utc_time.replace(tzinfo=pytz.utc)

    print(f"UTC time: {utc_time}")
    print(f"Local time: {args.local_time}")
    offset = (args.local_time - args.utc_time).total_seconds()
    offset_hours = int(offset // 60 // 60)
    offset_minutes = int(offset // 60 - offset_hours * 60)
    print(f"Offset:", end=" ")
    print("+" if offset_hours + offset_minutes >= 0 else "-", end="")
    print(f'{"0" if offset_hours <= 9 else ""}{offset_hours}', end=":")
    print(f'{"0" if offset_minutes <= 9 else ""}{offset_minutes}')

    possible_timezones = []

    for timezone in pytz.all_timezones:
        tz = pytz.timezone(timezone)
        local = utc_time.astimezone(tz)
        diff_minutes = (tz.localize(args.local_time) - local).total_seconds() / 60
        if abs(diff_minutes) <= args.allowed_delta:
            possible_timezones.append((timezone, diff_minutes))

    print(f"Possible locations ({len(possible_timezones)}):")
    for timezone, delta in sorted(possible_timezones, key=lambda e: e[1]):
        print(f"- {timezone} (delta {delta} min)")
