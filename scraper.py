import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import re


if __name__ == "__main__":
    print("What is the course syllabus link?")
    print("- For example: 'https://canvas.instructure.com/courses/5755799/assignments/syllabus'")
    syllabus = input("> ")
    print(syllabus)
