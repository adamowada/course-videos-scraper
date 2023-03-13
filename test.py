import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import re


async def parse_best_books(playwright):
    """
    """
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()

    # Get page content
    await page.goto("https://www.goodreads.com/choiceawards/best-books-2021")
    content = await page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(content, features="html.parser")
    books = [element.contents[1] for element in soup.find_all("div", class_="category clearFix")]
    category_links = {book.get_text().strip(): f"https://www.goodreads.com{book.attrs['href']}" for book in books}

    # Verify results and close browser
    print(category_links)
    await browser.close()
    return category_links


async def parse_category(playwright, url):
    """
    """
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()

    # Get page content
    await page.goto(url)
    content = await page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(content, features="html.parser")
    book = soup.find("a", class_="winningTitle choice gcaBookTitle")
    title = book.get_text()
    link = "https://www.goodreads.com" + book.attrs["href"]

    # Verify results and close browser
    print((title, link))
    await browser.close()
    return (title, link)


async def parse_book(playwright, url):
    """
    """
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()

    # Get page content
    await page.goto(url)
    content = await page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(content, features="html.parser")
   
    # Get star rating with backup method depending on page content
    stars = re.search(r"Average rating of (\S*)", str(soup))
    if stars:
        stars = stars.group(1)
    else:
        stars = soup.find("div", class_="uitext stacked").contents[5].get_text().strip()

    # Get ISBN number with backup method depending on page content
    isbn = re.search(r"\"isbn\":\"(\d*)", str(soup))
    if isbn:
        isbn = isbn.group(1)
    else:
        isbn = soup.find("div", id="bookDataBox").contents[3].span.span.get_text()

    # Verify results and close browser
    print(stars, isbn)
    await browser.close()
    return {
        "stars": stars,
        "isbn": isbn
    }


async def main():
    async with async_playwright() as playwright:
        # Get dictionary of categories and category links
        category_links = await parse_best_books(playwright)

        # Get dictionary of book titles and book links
        book_links = {book[0]: book[1] for link in category_links.values() if (book := await parse_category(playwright, link))}
        print(book_links)

        # test = {'Beautiful World, Where Are You': 'https://www.goodreads.com/book/show/56597885-beautiful-world-where-are-you?from_choice=true', 'The Last Thing He Told Me': 'https://www.goodreads.com/book/show/58744977-the-last-thing-he-told-me?from_choice=true', 'Malibu Rising': 'https://www.goodreads.com/book/show/58745185-malibu-rising?from_choice=true', 'A \u200bCourt of Silver Flames': 'https://www.goodreads.com/book/show/53138095-a-court-of-silver-flames?from_choice=true', 'People We Meet on Vacation': 'https://www.goodreads.com/book/show/54985743-people-we-meet-on-vacation?from_choice=true', 'Project Hail Mary': 'https://www.goodreads.com/book/show/54493401-project-hail-mary?from_choice=true', 'The Final Girl Support Group': 'https://www.goodreads.com/book/show/55829194-the-final-girl-support-group?from_choice=true', 'Broken': 'https://www.goodreads.com/book/show/54305363-broken?from_choice=true', 'The Anthropocene Reviewed': 'https://www.goodreads.com/book/show/55145261-the-anthropocene-reviewed?from_choice=true', 'Crying in H Mart': 'https://www.goodreads.com/book/show/54814676-crying-in-h-mart?from_choice=true', 'Empire of Pain: The Secret History of the Sackler Dynasty': 'https://www.goodreads.com/book/show/43868109-empire-of-pain?from_choice=true', 'Lore Olympus: Volume One': 'https://www.goodreads.com/book/show/57282218-lore-olympus?from_choice=true', 'The Hill We Climb: An Inaugural Poem for the Country': 'https://www.goodreads.com/book/show/56914101-the-hill-we-climb?from_choice=true', 'The Spanish Love Deception': 'https://www.goodreads.com/book/show/57190892-the-spanish-love-deception?from_choice=true', "Firekeeper's Daughter": 'https://www.goodreads.com/book/show/57812106-firekeeper-s-daughter?from_choice=true', 'Rule of Wolves': 'https://www.goodreads.com/book/show/54589790-rule-of-wolves?from_choice=true', 'Daughter of the Deep': 'https://www.goodreads.com/book/show/57094644-daughter-of-the-deep?from_choice=true'}

        # Get dictionary of star rating and ISBN number
        # result = await parse_book(playwright, "https://www.goodreads.com/book/show/56597885-beautiful-world-where-are-you?from_choice=true")
        # print(result)
        book_data = [await parse_book(playwright, url) for url in book_links.values()]
        print(book_data)
        

asyncio.run(main())