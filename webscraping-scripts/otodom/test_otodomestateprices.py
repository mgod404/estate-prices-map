from otodomestateprices import otodom_page_scraper, how_many_pages_to_scrape
import unittest


URL = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?limit=500&page="
class TestOtodomEstatePrices(unittest.TestCase):
    def test_how_many_pages_to_scrape(self):
        self.assertTrue(type(how_many_pages_to_scrape(URL)) == int and how_many_pages_to_scrape(URL) > 0)
    def test_otodom_page_scraper(self):
        self.assertTrue(len(otodom_page_scraper(1,URL)) > 1)

if __name__ == '__main__':
    unittest.main()
