from datetime import datetime


def generate_datetime() -> str:
    date: datetime = datetime.now()
    formatted_output: str = (
        date.strftime("%B ") 
        + str(date.day) 
        + date.strftime(", %Y")
    )
    return formatted_output


# EOSC