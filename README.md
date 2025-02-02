# Reklama5scraper

## Description
Reklama5 Scraper is a Python-based GUI application built with PySimpleGUI that allows users to scrape classified ads from the website **Reklama5**. It enables users to select categories and subcategories, specify keywords for filtering ads, and export the results to an Excel file.

## Features
- Select **categories and subcategories** dynamically.
- Scrape ads from multiple pages concurrently for faster performance.
- **Keyword filtering**: Search for keywords in ad titles and descriptions.
- **Progress tracking**:
  - Progress bar for pages fetched.
  - Progress bar for keyword searches.
- Export filtered ads to an **Excel file**.

## Dependencies
Ensure you have the following Python libraries installed before running the script:

```sh
pip install PySimpleGUI pandas requests beautifulsoup4 openpyxl
```

## How It Works

1. **Select a category**: Click a button corresponding to the desired category.
2. **Choose a subcategory** (if available) from the dropdown menu.
3. **Specify search keywords**: Enter keywords separated by commas. The app automatically searches in both Latin and Macedonian.
4. **Set the number of pages**: Adjust the slider to define how many pages should be scraped.
5. **Choose search criteria**:
   - Search in ad titles
   - Search in ad descriptions
   - Search in both
6. **Fetch ads**: Click "Провери реклами" to start scraping ads.
7. **Filter results**: Click "Прикажи реклами" to display ads that match the search criteria.
8. **Export to Excel**: Click "Експортирај во Excel" to save matched ads as an Excel file.

## Code Overview

### Main Components:
- **GUI Layout**: Built using PySimpleGUI.
- **Scraping Functions** (from `Reklama5_Scraper` module):
  - `page_read(url, max_pages)`: Fetches ad links from multiple pages.
  - `fetch_ad_details(link)`: Extracts details (title, price, description, link) from an ad.
- **Multithreading**:
  - Uses `ThreadPoolExecutor` for concurrent scraping.
  - Implements `threading.Thread` to avoid GUI freezing.
- **Progress Updates**:
  - Uses `window.write_event_value()` to update progress bars dynamically.

## Notes
- The script resets the progress bars when selecting a new category.
- Progress updates for **page fetching** occur incrementally to avoid UI lag.
- Keyword searches update progress dynamically while processing ads.

## Running the Script
Simply run the Python script:

```sh
python reklama5_scraper.py
```

## Future Improvements
- Add support for additional filtering options (price range, date posted, etc.).
- Optimize UI performance for large datasets.
- Implement automatic updates for new categories.

---
This README provides an overview of the Reklama5 Scraper, its functionality, and how to use it effectively. 🚀

