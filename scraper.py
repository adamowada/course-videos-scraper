import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import re


async def parse_zoom_links(playwright, syllabus):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()

    # Get page content
    await page.goto(syllabus)
    
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
