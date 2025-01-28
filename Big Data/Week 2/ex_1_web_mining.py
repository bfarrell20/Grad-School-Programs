#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def init_url(): #initial url
    return "https://aliceinwonderland.fandom.com/wiki/Alice_in_Wonderland_Wiki"

def books():
    url = init_url() #get initial url
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, "lxml")

    # Find the Literature dropdown to start process
    all_dropdowns = soup.find_all("li", {"class": "wds-dropdown"})
    literature_dropdown = None
    for dropdown in all_dropdowns:
        # Check if the dropdown contains the text "Literature"
        if dropdown.find("span", string="Literature"):
            literature_dropdown = dropdown
            break

    if literature_dropdown:
        # Find Canon books section next
        canon_books_section = literature_dropdown.find("span", string="Canon books")

        if canon_books_section:
            # Find where the list of books is inside the canon books section
            canon_books_list = canon_books_section.find_next("ul", {"class": "wds-list wds-is-linked"})

            if canon_books_list:
                # Add all the books into a list
                canon_books = []
                for book in canon_books_list.find_all("a"):
                    title = book.get_text(strip=True)
                    canon_books.append(title)

    return canon_books

def poems():
    # initial url
    url = init_url()
    poems = []
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the Literature dropdown
    all_dropdowns = soup.find_all("li", {"class": "wds-dropdown"})
    literature_dropdown = None
    for dropdown in all_dropdowns:
        if dropdown.find("span", string="Literature"):
            literature_dropdown = dropdown
            break

    if literature_dropdown:
        # Find the Poems section
        poems_section = literature_dropdown.find("span", string="Canon poems")

        if poems_section:
            # Find the list of poems inside the poem section
            poems_list = poems_section.find_next("ul", {"class": "wds-list wds-is-linked"})

            if poems_list:
                # Get all the poem titles and links into a list
                for poem in poems_list.find_all("a"):
                    title = poem.get_text(strip=True)
                    link = poem.get('href')
                    entry = (title, link)
                    poems.append(entry)

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
    # Find the poem text for the the two poems that use this format (according to the instructions)
    poem_page = soup.find("span", {"class": "mw-headline"}, string = "Text")

    if poem_page:
        for p in poem_page.find_all_next("p"):#find the text under the p tags
            if p.find_previous("h2") != poem_page.find_parent("h2"):
                break

            # Append all the text together 
            poem_full_text += p.get_text(strip=True) + "\n"
    else:
        print("Poem header not found.")
    poem_info = (poems[n][0], poem_full_text) #create tuple with poem title and text inside
    poem_return.append(poem_info)
    return poem_return