import time
import validators
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Assignment:
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.minimize_window()
        self.link = input("Enter a Wikipedia link: ").strip()
        self.unique_links = set()
        self.file_path = Path('unique_links.txt')
        self.file_path.write_text('')

    def validate_wiki_link(self):
        if not validators.url(self.link):
            print("The link format is invalid.")
            self.driver.quit()
            exit()
        self.driver.maximize_window()
        wiki_link = 'en.wikipedia.org'
        self.driver.get(self.link)
        time.sleep(3)
        current_url = self.driver.current_url
        try:
            assert wiki_link in current_url, "Not a valid wikipedia page"
            print("The link is a valid Wikipedia link.")
        except AssertionError as e:
            print(e)
            self.driver.quit()
            exit()
        self.driver.minimize_window()

    @staticmethod
    def accept_integer():
        try:
            n = int(input("Enter an integer between 1 to 3:  "))
            assert isinstance(n, int) and 1 <= n <= 3, f"Number {n} is not accepted."
            print("Number is accepted")
            return n
        except AssertionError as e:
            print(e)
            return None

    time.sleep(3)

    def scrape_wiki_links(self, n):
        for _ in range(n):
            self.driver.maximize_window()
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            all_links = soup.find_all('a', href=True)
            max_links = 10
            time.sleep(3)
            try:
                # Extract and filter unique Wikipedia links
                links_this_run = set()
                for a_tag in all_links:
                    href = a_tag['href']
                    if href.startswith('/wiki/') and len(links_this_run) < 10:
                        full_link = f"https://en.wikipedia.org{href}"
                        if full_link not in self.unique_links and full_link not in links_this_run:
                            links_this_run.add(full_link)
                self.unique_links.update(links_this_run)

            except Exception as e:
                print(f"An error occurred: {e}")

        self.driver.quit()
        with self.file_path.open('a') as file:  # Open file in append mode
            for link in self.unique_links:
                file.write(link + '\n')
        print(f"File path: {self.file_path.resolve()}")


if __name__ == "__main__":
    assignment_instance = Assignment()
    assignment_instance.validate_wiki_link()
    number = assignment_instance.accept_integer()
    if number is not None:
        assignment_instance.scrape_wiki_links(number)
    else:
        print("Exiting due to invalid number.")
