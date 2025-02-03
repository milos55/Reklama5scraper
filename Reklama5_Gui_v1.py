# Reklama 5 scraper
# Author: Milosh Smiljkovikj
# Date: 29/01/2025
# Description: Proverka na reklami objaveni na reklama 5 so izbor na del od opisot

import PySimpleGUI as sg
import concurrent.futures
import Reklama5_Scraper_v1 as rs  # Assuming you imported your functions and dicts as rs
import threading
import pandas as pd
import time
from os import cpu_count

max_workers = cpu_count() * 2  # Increase workers for better parallelism

def main_gui():
    sg.theme('DarkGrey1')

    # Layout for category buttons (5 buttons per row)
    category_buttons = [
        [sg.Button(category, size=(20, 2), key=category) for category in list(rs.katdict.keys())[i:i+5]]
        for i in range(0, len(rs.katdict), 5)
    ]
    
    # Layout
    layout = [
        [sg.Text("Избери категорија:")],
        *category_buttons,
        [sg.Text("Избери подкатегорија:"), sg.Combo([], key="-SUBCATEGORY-")],
        [sg.Text("Внеси зборови за пребарување:"), sg.InputText("", key="-KEYWORDS-"), sg.Text("Само со латински букви, автоматски бара и на македонски", text_color="honeydew1")],
        [sg.Text("Број на страни"), sg.Slider((1, 150), 30, orientation='horizontal', key="-PAGES-")],
        [sg.Button("Провери реклами"), sg.Button("Прикажи реклами"), sg.Button("Излез")],
        [sg.Checkbox("Барај по наслов", key="-TITLE-"),
         sg.Checkbox("Барај по опис", key="-DESC-"),
         sg.Checkbox("Барај по двете", key="-ALL-", default=True)],
        [sg.Output(size=(120, 20))],  # For displaying outputs
        [sg.Text("Progress of pages fetched:"), sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PAGE_PROGRESS-"), sg.Text("Кликни прикажи реклами за да се прикажат!", text_color="honeydew1")],
        [sg.Text("Progress of ads searched:"), sg.ProgressBar(100, orientation='h', size=(20, 20), key="-AD_PROGRESS-"), sg.Button("Експортирај во Excel")]
    ]

    window = sg.Window("Reklama5 Scraper", layout)

    ads = []  # Store scraped ads
    selected_category = None
    selected_subcategory = None

    def fetch_ads_and_update_progress():
        window["Провери реклами"].update(disabled=True)
        window["Прикажи реклами"].update(disabled=True)
        window["Експортирај во Excel"].update(disabled=True)
        nonlocal ads

        if not selected_category:
            window["Провери реклами"].update(disabled=False)
            print("Не одбра категорија.")
            return

        subcategory = values["-SUBCATEGORY-"] if values["-SUBCATEGORY-"] else selected_subcategory
        if not subcategory:
            window["Провери реклами"].update(disabled=False)
            print("Не одбра подкатегорија.")
            return

        max_pages = int(values["-PAGES-"])
        primary_value = rs.katdictx.get(rs.katdict[selected_category], {})
        if isinstance(primary_value, dict):
            secondary_url = primary_value.get(subcategory, "")
        else:
            secondary_url = primary_value

        if secondary_url:
            ad_links = rs.page_read(secondary_url, max_pages)

            # Set progress bar max value based on total pages
            window["-PAGE_PROGRESS-"].update(0, max=max_pages)

            for i, link in enumerate(ad_links):
                # Fetch ad details for the current page
                ads_on_page = rs.fetch_ad_details(link)  
                
                if ads_on_page:  # Only update progress if ads were actually fetched
                    window.write_event_value("-PROGRESS_PAGE-", i + 1)
                
                time.sleep(0.1)  # Simulate delay (remove this in actual implementation)


            # Use ThreadPoolExecutor for fetching ad details concurrently
            ads = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(rs.fetch_ad_details, link): link for link in ad_links}
                for future in concurrent.futures.as_completed(futures):
                    ads.append(future.result())

            window["Провери реклами"].update(disabled=False)
            window["Прикажи реклами"].update(disabled=False)
            window["Експортирај во Excel"].update(disabled=False)

            if not ads:  # Only print if no ads have been fetched yet
                print(f"\nПрибрани {len(ads)} реклами!")

    def search_ads_and_update_progress():
        matched_ads = []  # Store only the matched ads

        if ads:
            # Initialize the progress bar max value to total number of ads
            window["-AD_PROGRESS-"].update(0, max=len(ads))  # Set max to the number of ads
            keywords = [keyword.strip().lower() for keyword in values["-KEYWORDS-"].split(",")]  # Lowercase and strip extra spaces
            all_keywords = []

            for keyword in keywords:
                all_keywords.append(keyword)  # Add the original keyword (in Latin)
                all_keywords.append(rs.transliterate_to_macedonian(keyword))  # Add the Macedonian version

            print("Бара за", all_keywords, "\n")

            # Iterate over each ad and match keywords
            for i, ad in enumerate(ads):
                match_found = False

                # Title search logic
                if values["-TITLE-"]:
                    for keyword in all_keywords:
                        if keyword in ad.get("adtitle", "").lower():
                            match_found = True
                            break  # Stop if a match is found

                # Description search logic
                if values["-DESC-"]:
                    for keyword in all_keywords:
                        if keyword in ad.get("addesc", "").lower():
                            match_found = True
                            break  # Stop if a match is found

                # Search in both title and description
                if values["-ALL-"]:
                    for keyword in all_keywords:
                        if keyword in ad.get("adtitle", "").lower() or keyword in ad.get("addesc", "").lower():
                            match_found = True
                            break  # Stop if a match is found

                if match_found:
                    matched_ads.append(ad)  # Add the matched ad to the matched_ads list

                    print(f"Наслов: {ad['adtitle']}")
                    print(f"Цена: {ad['adprice']}")
                    print(f"Линк: {ad['adlink']}")
                    print("---")  # Separate the ads with a line

                # Update the progress bar for each ad processed
                if i % 2 == 0:  # Updates every 2 ads
                    window.write_event_value("-PROGRESS_AD-", i + 1)

            print(f"\nПронајдени {len(matched_ads)} реклами!")  # Print number of matched ads


    def export_to_excel():
        if not ads:
            sg.popup("Нема податоци за експортирање!")
            return

        # Filter ads based on keyword matching logic
        keywords = [keyword.strip().lower() for keyword in values["-KEYWORDS-"].split(",")]
        
        matched_ads = []  # Ensure this is defined inside the function
        for ad in ads:
            match_found = False

            if values["-TITLE-"]:
                for keyword in keywords:
                    if keyword in ad.get("adtitle", "").lower():
                        match_found = True
                        break  # Stop if a match is found

            if values["-DESC-"]:
                for keyword in keywords:
                    if keyword in ad.get("addesc", "").lower():
                        match_found = True
                        break  # Stop if a match is found

            if values["-ALL-"]:
                for keyword in keywords:
                    if keyword in ad.get("adtitle", "").lower() or keyword in ad.get("addesc", "").lower():
                        match_found = True
                        break  # Stop if a match is found

            if match_found:
                matched_ads.append({
                    "ADNAME": ad.get("adtitle"), 
                    "PRICE": ad.get("adprice"), 
                    "LINK": ad.get("adlink")
                })

        if not matched_ads:
            sg.popup("Нема реклами кои одговараат на критериумите!")
            return

        # Convert the matched ads to DataFrame
        df = pd.DataFrame(matched_ads)

        filename = sg.popup_get_file("Зачувај како", save_as=True, default_extension=".xlsx", file_types=(('Excel Files', '*.xlsx'),))
        if filename:
            df.to_excel(filename, index=False)
            sg.popup("Успешно зачувано!")

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Излез"):
            break

        # When category is selected, update subcategory list or fetch base value
        if event in rs.katdict:  # category button pressed
            selected_category = event
            primary_value = rs.katdictx.get(rs.katdict[selected_category], {})
            
            window["-PAGE_PROGRESS-"].update(0, max=len(ads))
            window["-AD_PROGRESS-"].update(0, max=len(ads))

            if isinstance(primary_value, dict):  # If subcategories exist
                subcategories = list(primary_value.keys())
                window["-SUBCATEGORY-"].update(values=subcategories)
                print(f"Одберена категорија: {selected_category}\n")
            else:  # If no subcategories, use the base value directly
                selected_subcategory = primary_value
                window["-SUBCATEGORY-"].update(values=[])  # Clear subcategory selection
                print(f"Одберена категорија: {selected_category} (Нема подкатегории) \n")
        
        # Провери реклами
        if event == "Провери реклами":
            threading.Thread(target=fetch_ads_and_update_progress, daemon=True).start()

        # Keyword Search
        if event == "Прикажи реклами"
            threading.Thread(target=search_ads_and_update_progress, daemon=True).start()

        # Export to Excel
        if event == "Експортирај во Excel":
            export_to_excel()

        # Handle progress updates for pages and ads
        if event == "-PROGRESS_PAGE-":
            window["-PAGE_PROGRESS-"].update(values["-PROGRESS_PAGE-"])

        if event == "-PROGRESS_AD-":
            window["-AD_PROGRESS-"].update(values["-PROGRESS_AD-"])

        window.refresh()

    window.close()

if __name__ == "__main__":
    main_gui()
