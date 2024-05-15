from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
import re

# bachelor 3/4/5/6
# master 1/2/autumn/spring

COLUMNS = pd.MultiIndex.from_tuples([('Code', ''), ('Title', ''), ('Language', ''), 
                                     ('Sem 1', 'L'), ('Sem 1', 'E'), ('Sem 1', 'P'),
                                     ('Sem 2', 'L'), ('Sem 2', 'E'), ('Sem 2', 'P'),
                                     ('Sem 3', 'L'), ('Sem 3', 'E'), ('Sem 3', 'P'),
                                     ('Sem 4', 'L'), ('Sem 4', 'E'), ('Sem 4', 'P'),
                                     ('Specialisations', ''), ('Exam', ''), ('Credits', '')])
DIR_FILES = Path(__file__).parent / 'file'
html_files = DIR_FILES.glob("*.html")
OUT_FILEPATH = Path(__file__).parent / 'out.xlsx'

def extract_data(soup: BeautifulSoup):
    courses = soup.find_all('div', class_='line')
    data = []
    for course in courses:
        cours = course.contents[0]
        language = course.contents[1]
        semesters = course.find_all('div', class_='bachlor')
        exam = course.contents[-3]
        credits = course.contents[-2]

        sems = []
        for semester in semesters:
            l, e, p = [_.contents[0] if len(_.contents) == 1 else _.contents[1] for _ in semester.find_all('div', class_='cep')]
            sems += [{'L': l, 'E': e, 'P': p}]
        while(len(sems) < 4):
            sems += [{'L': '-', 'E': '-', 'P': '-'}]
        
        match = re.search(r"[A-Z]+-\d+", cours.contents[1].contents[0])
        code = match.group(0) if match is not None else "N/A"
        title = f'=HYPERLINK("{cours.contents[0].a.attrs["href"]}", "{cours.contents[0].a.contents[0]}")'
        lang = language.abbr.contents[0]
        if exam.b is not None:
            exam = exam.b.contents[0] + ' / ' + exam.span.contents[0] if len(exam.span.contents) > 0 else exam.b.contents[0]
        else:
            exam = ""
        credits = int(credits.div.contents[0])

        # code, title, lang, l1, e1, p1, l2, e2, p2, l3, e3, p3, l4, e4, p4, spec, exam, credits = extract_data(soup)
        data.append({"Code": code, "Title": title, "Language": lang, "Sem 1": sems[0], "Sem 2": sems[1], "Sem 3": sems[2], "Sem 4": sems[3], "Exam": exam, "Credits": credits})
        pass
        
    return data

def main():
    excel_writer = pd.ExcelWriter(OUT_FILEPATH, engine='xlsxwriter')
    all_df = pd.DataFrame()
    
    for path in html_files:
        file = open(Path(path))
        soup = BeautifulSoup(file, features='html.parser')
        file.close()
        
        df = pd.DataFrame(extract_data(soup))
        all_df = pd.concat([all_df, df])
        df.to_excel(excel_writer, sheet_name=path.stem, index=False)
    
    all_df = all_df.drop_duplicates("Code")
    all_df.to_excel(excel_writer, sheet_name='All', index=False)
    excel_writer.close()


if __name__ == '__main__':
    main()
    print("Finished!")
