import os

import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright


load_dotenv()


async def parse_zoom_links(playwright, syllabus):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()

    # Login and get page content
    await page.set_viewport_size({"width": 640, "height": 480})
    await page.goto(syllabus)
    await page.click("#pseudonym_session_unique_id")
    await page.type("#pseudonym_session_unique_id", os.getenv("EMAIL"))
    await page.click("#pseudonym_session_password")
    await page.type("#pseudonym_session_password", os.getenv("PASSWORD"))
    await page.pause()
    await page.click(".Button Button--login")
    content = await page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(content, features="html.parser")
    links = [element for element in soup.find_all("a")]
    return links


async def main():
    print("What is the course syllabus link?")
    print("- For example: 'https://canvas.instructure.com/courses/5755799/assignments/syllabus'")
    syllabus = input("> ")
    print(syllabus)
    async with async_playwright() as playwright:
        #
        content = await parse_zoom_links(playwright, syllabus)
        print(content)


if __name__ == "__main__":
    asyncio.run(main())
