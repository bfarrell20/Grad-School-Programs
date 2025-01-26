#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# URL of the Alice in Wonderland Wikipedia page
def init_url():
    return "https://aliceinwonderland.fandom.com/wiki/Alice_in_Wonderland_Wiki"

def books():
    # Send a GET request to fetch the page content
    url = init_url()
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the "Literature" dropdown
    all_dropdowns = soup.find_all("li", {"class": "wds-dropdown"})
    literature_dropdown = None
    for dropdown in all_dropdowns:
        # Check if the dropdown contains the text "Literature"
        if dropdown.find("span", string="Literature"):
            literature_dropdown = dropdown
            break

    if literature_dropdown:
        # Find the "Canon books" section within the dropdown
        canon_books_section = literature_dropdown.find("span", string="Canon books")

        if canon_books_section:
            # Navigate to the nested list of canon books
            canon_books_list = canon_books_section.find_next("ul", {"class": "wds-list wds-is-linked"})

            if canon_books_list:
                # Extract all book titles
                canon_books = []
                for book in canon_books_list.find_all("a"):
                    title = book.get_text(strip=True)
                    canon_books.append(title)

    return canon_books

def poems():
    # Send a GET request to fetch the page content
    url = init_url()
    poems = []
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the "Literature" dropdown
    all_dropdowns = soup.find_all("li", {"class": "wds-dropdown"})
    literature_dropdown = None
    for dropdown in all_dropdowns:
        # Check if the dropdown contains the text "Literature"
        if dropdown.find("span", string="Literature"):
            literature_dropdown = dropdown
            break

    if literature_dropdown:
        # Find the "Poems" section within the dropdown
        poems_section = literature_dropdown.find("span", string="Canon poems")

        if poems_section:
            # Navigate to the nested list of poems
            poems_list = poems_section.find_next("ul", {"class": "wds-list wds-is-linked"})

            if poems_list:
                # Extract all poem titles
                for poem in poems_list.find_all("a"):
                    title = poem.get_text(strip=True)
                    link = poem.get('href')
                    entry = (title, link)
                    poems.append(entry)

                # Print the list of poems
    #print(poems)
    return poems

def poem_title_text(poemlist, n):
    poems = poemlist
    url = poems[n][1]
    poem_full_text = ""
    poem_return = []
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    soup = BeautifulSoup(html_content, "html.parser")
    # Find the poem text
    poem_page = soup.find("span", {"class": "mw-headline"}, string = "Text")

    if poem_page:
        for p in poem_page.find_all_next("p"):
            if p.find_previous("h2") != poem_page.find_parent("h2"):
                break

            # Append the text of each <p> tag to the full poem text
            poem_full_text += p.get_text(strip=True) + "\n"
    else:
        print("Poem header not found.")
    poem_info = (poems[n][0], poem_full_text)
    poem_return.append(poem_info)
    return poem_return


# books()
poem_list = poems()
print(poem_title_text(poem_list, 5))