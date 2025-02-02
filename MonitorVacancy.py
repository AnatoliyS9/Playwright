from calendar import month

from playwright.sync_api import Playwright, sync_playwright, expect
import string
import random
from datetime import datetime
import re

with (sync_playwright() as playwright):
    # Словарь с месяцами на украинском языке
    months_ua = {
        1: "січня",
        2: "лютого",
        3: "березня",
        4: "квітня",
        5: "травня",
        6: "червня",
        7: "липня",
        8: "серпня",
        9: "вересеня",
        10: "жовтеня",
        11: "листопада",
        12: "груденя"
    }

    # Текущая дата
    now = datetime.now()
    day = now.day
    month = months_ua[now.month]
    target_date = str(day) + ' ' + month
    # Результат

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://dou.ua/")
    page.get_by_role("link", name="Робота").first.click()
    page.get_by_label("Категорія").click()
    page.select_option('select[name="category"]', 'QA')
    page.wait_for_timeout(3000)

    vacancy_items = page.query_selector_all(".l-vacancy")

    found = False  # Переменная для отслеживания, были ли найдены вакансии с нужной датой

    # Перебираем все вакансии и выводим только те, у которых дата "31 січня"
    for vacancy in vacancy_items:
        # Извлекаем дату
        date_element = vacancy.query_selector(".date")

        if date_element:
            date_text = date_element.text_content().strip()

            if date_text == target_date:
                # Извлекаем title и company
                title_element = vacancy.query_selector(".title a")
                company_element = vacancy.query_selector(".company")

                if title_element and company_element:
                    title = title_element.text_content().strip()
                    company = company_element.text_content().strip()

                    # Выводим данные в одну строку
                    print(f"{date_text} {title} {company}")
                    found = True

    if not found:
        print("Date not found")

    browser.close()
