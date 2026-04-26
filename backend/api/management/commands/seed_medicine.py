import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from api.Medicine.model import Medicine

BASE_URL = "http://www.homeoint.org/books/boericmm"
INDEX_PAGES = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]


class Command(BaseCommand):
    help = 'Scrape medicine data from homeoint.org and seed into Medicine model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--letters', nargs='+', default=INDEX_PAGES,
            help='Letters to scrape (e.g. --letters a b c)'
        )

    def handle(self, *args, **kwargs):
        letters = kwargs['letters']
        created, skipped = 0, 0

        for letter in letters:
            index_url = f"{BASE_URL}/{letter}.htm"
            self.stdout.write(f"Fetching index: {index_url}")

            try:
                res = requests.get(index_url, timeout=10)
                res.raise_for_status()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Skipped index {letter}: {e}"))
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            links = list(dict.fromkeys(
                a["href"] for a in soup.find_all("a", href=True)
                if a["href"].startswith(f"{letter}/")
            ))

            for href in links:
                med_url = f"{BASE_URL}/{href}"
                try:
                    med_res = requests.get(med_url, timeout=10)
                    med_res.raise_for_status()
                    med_soup = BeautifulSoup(med_res.text, "html.parser")

                    # Title: from <title> tag, take part before first ' - '
                    page_title = med_soup.title.get_text(strip=True) if med_soup.title else ""
                    title = page_title.split(" - ")[0].strip() if " - " in page_title else href

                    # Description: everything after the medicine name anchor tag, skip title and copyright
                    anchor = med_soup.find("a", attrs={"name": True})
                    if anchor:
                        parts = [t.strip() for t in anchor.find_all_next(string=True) if t.strip()]
                        # skip first 2 parts (medicine name + common name)
                        parts = parts[2:]
                        # remove copyright from end
                        if parts and parts[-1] == "Home":
                            parts = parts[:-1]
                        while parts and parts[-1].startswith("Copyright"):
                            parts = parts[:-1]
                        description = " ".join(parts)
                    else:
                        description = ""

                    if Medicine.objects.filter(medicine_name=title).exists():
                        self.stdout.write(f"  Skipped (exists): {title}")
                        skipped += 1
                        continue

                    Medicine.objects.create(
                        medicine_name=title,
                        full_description=description,
                    )
                    self.stdout.write(self.style.SUCCESS(f"  Created: {title}"))
                    created += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  Error on {med_url}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {created}, Skipped: {skipped}"
        ))
