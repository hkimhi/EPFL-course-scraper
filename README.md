# EPFL Course Scraper

Basic project to scrape EPFL course information. Made for personal use to figure out which courses to take while on an exchange semester at EPFL during the 2023-2024 spring semester.

HTML pages for the degree cycles were downloaded and put in `file/` so I didn't have to deal with web requests and so I could work on the plane trip across the Atlantic.

Each degree cycle got its own sheet within the `out.xlsx` spreadsheet, and all courses were added to a sheet called **all** within `out.xlsx` spreadsheet, removing duplicates. Storing into a spreadsheet with chosen so I could use the built-in filtering mechanisms of spreadsheet software like LibreOffice Calc.
