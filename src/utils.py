from datetime import datetime, UTC


def generate_datetime() -> str:
    date: datetime = datetime.now(UTC)
    return f"{date.strftime('%B')} {date.day}, {date.year}"


# EOSC