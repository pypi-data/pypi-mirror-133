from dataclasses import dataclass
from datetime import date
from textwrap import dedent


@dataclass
class Work:
    name: str
    url: str
    start: date
    end: date = None


name = "Julian Wachholz"
username = "julianwachholz"

work = ["inaffect", "Quatico", "Avectris", "Polynorm", "Unic"]
work = [
    Work("inaffect", "https://inaffect.net/", date(2021, 6, 1)),
    Work("Quatico", "https://www.quatico.com/", date(2020, 5, 1), date(2021, 5, 1)),
    Work("Avectris", "https://aveniq.ch/", date(2019, 5, 1), date(2020, 2, 1)),
    Work("Polynorm", "https://polynorm.ch/", date(2015, 6, 1), date(2019, 4, 1)),
    Work("Unic", "https://unic.com/", date(2011, 3, 1), date(2014, 7, 1)),
]

website = "https://julianwachholz.dev"
twitter = "https://twitter.com/julianwachholz"
github = "https://github.com/julianwachholz"

email = "julian@wachholz.ch"
pgp = "https://julianwachholz.dev/julian_wachholz_pub.asc"


def card():
    print(
        dedent(
            f"""
            {name} / @{username}

            Website: {website}
            Twitter: {twitter}
            GitHub:  {github}
            Work:    {work[0].url}

            Mail:    {email}
                     (PGP: {pgp})

            Card:    pipx run jwa
            """
        )
    )


if __name__ == "__main__":
    card()
