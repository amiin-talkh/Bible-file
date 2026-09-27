import os
import re
from bs4 import BeautifulSoup

# Замыг өөрийн бодит зам руу зөв зааж өгнө үү
base_folder = r"C:\Users\Amiin Talkh\Desktop\mn_new\mn_new"
output_file = "easyworship_bible.txt"

# 66 номын стандарт монгол нэрсийг дугаараар нь тохируулах (Найдвартай шийдэл)
BIBLE_BOOKS = {
    "01": "Эхлэл", "02": "Египетээс гарсан нь", "03": "Левит", "04": "Тооллого", "05": "Дэд хууль",
    "06": "Иошуа", "07": "Шүүгчид", "08": "Рут", "09": "1 Самуел", "10": "2 Самуел",
    "11": "1 Хаад", "12": "2 Хаад", "13": "1 Шастир", "14": "2 Шастир", "15": "Езра",
    "16": "Нехемиа", "17": "Естер", "18": "Иов", "19": "Дуулал", "20": "Сургаалт үгс",
    "21": "Номлогчийн үгс", "22": "Соломоны дуу", "23": "Исаиа", "24": "Иеремиа", "25": "Гашуудал",
    "26": "Езекиел", "27": "Даниел", "28": "Хосеа", "29": "Иоел", "30": "Амос",
    "31": "Обадиа", "32": "Иона", "33": "Миха", "34": "Нахум", "35": "Хабакук",
    "36": "Цефаниа", "37": "Хагаи", "38": "Захариа", "39": "Малахи", "40": "Матай",
    "41": "Марк", "42": "Лук", "43": "Иохан", "44": "Үйлс", "45": "Ром",
    "46": "1 Коринт", "47": "2 Коринт", "48": "Галат", "49": "Ефес", "50": "Филиппой",
    "51": "Колоссай", "52": "1 Фессалоник", "53": "2 Фессалоник", "54": "1 Тимот", "55": "2 Тимот",
    "56": "Тит", "57": "Филимон", "58": "Мөргөл", "59": "Иаков", "60": "1 Петр",
    "61": "2 Петр", "62": "1 Иохан", "63": "2 Иохан", "64": "3 Иохан", "65": "Иуда", "66": "Илчлэлт"
}

with open(output_file, "w", encoding="utf-8") as out_f:
    
    # Хавтас бүрээр гүйх
    for book_folder in sorted(os.listdir(base_folder)):
        if book_folder == "_assets" or book_folder.startswith("_"):
            continue
            
        book_path = os.path.join(base_folder, book_folder)
        
        if os.path.isdir(book_path):
            # Хавтасны дугаарыг салгаж авах (жишээ нь "01_Genesis" эсвэл "01" байвал -> "01")
            folder_num = re.findall(r'\d+', book_folder)
            
            book_name = "Тодорхойгүй"
            if folder_num:
                num_key = f"{int(folder_num[0]):02d}"  # 1 -> "01" болгоно
                book_name = BIBLE_BOOKS.get(num_key, book_folder)
            else:
                book_name = book_folder

            htm_files = sorted(
                [f for f in os.listdir(book_path) if f.endswith((".htm", ".html"))], 
                key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 999
            )

            print(f"Уншиж байна: {book_name} ({book_folder})")

            # Бүлгүүдээр (файл) гүйх
            for htm_file in htm_files:
                file_path = os.path.join(book_path, htm_file)
                
                # Файлын нэрнээс бүлгийн дугаарыг авах
                match = re.search(r'\d+', htm_file)
                if match:
                    chapter_num = str(int(match.group()))
                else:
                    continue
                
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    verses = soup.find_all('span', class_='verse')
                    
                    for verse in verses:
                        verse_id = verse.get('id')
                        if not verse_id: 
                            continue
                            
                        # Текстийг цэвэрлэх
                        text_parts = []
                        for sibling in verse.next_siblings:
                            if sibling.name == 'span' and 'verse' in sibling.get('class', []):
                                break 
                            
                            if isinstance(sibling, str):
                                text_parts.append(sibling.strip())
                            elif sibling.name not in ['br', 'span']:
                                text_parts.append(sibling.get_text(strip=True))
                        
                        clean_text = " ".join([t for t in text_parts if t])
                        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                        
                        # Эцсийн формат: Эхлэл 2:11 ...
                        if clean_text:
                            line = f"{book_name} {chapter_num}:{verse_id} {clean_text}\n"
                            out_f.write(line)

print(f"\nАмжилттай дууслаа! '{output_file}' файл цэвэрхэн болж үүслээ.")