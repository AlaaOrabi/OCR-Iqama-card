# Install Tesseract, including Arabic language data
!sudo apt install -y tesseract-ocr tesseract-ocr-ara

# Install Python libraries
!pip install pytesseract Pillow pandas openpyxl googletrans==4.0.0-rc1

from PIL import Image
import pytesseract
import pandas as pd
import re
from googletrans import Translator

# Load the image
image_path = 'iqama.jpg'
image = Image.open(image_path)

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image, lang='eng+ara')

# Function to convert Arabic numerals to English
def convert_arabic_to_english(arabic_number):
    arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    return arabic_number.translate(arabic_to_english)

# Extract relevant data from the text using regex

# Extract the name, assuming it's in English and using a flexible pattern
name_match = re.search(r'([A-Z]+\s[A-Z]+\s[A-Z]+\s[A-Z]+\s[A-Z]+)', text)
name = name_match.group(1).strip() if name_match else ""

# Extract the ID number
id_number_match = re.search(r'(\d{10})', text)
id_number = id_number_match.group(1) if id_number_match else ""

# Extract the issue place
issue_place_match = re.search(r'(?<=مكان الإصدار\s)(.*?)(?=\s)', text)
issue_place_ar = issue_place_match.group(1).strip() if issue_place_match else ""

# Extract the birth date
birth_date_match = re.search(r'(?<=للمبلاد \s)(\d{10})', text)
birth_date_ar = birth_date_match.group(1) if birth_date_match else ""
birth_date_en = convert_arabic_to_english(birth_date_ar)

# Extract the expiry date
expiry_date_match = re.search(r'(?<=الإنتهاء\s)(\d{10})', text)
expiry_date_ar = expiry_date_match.group(1) if expiry_date_match else ""
expiry_date_en = convert_arabic_to_english(expiry_date_ar)

# Extract the job title
job_title_match = re.search(r'(?<=انهنة\s)(.*?)(?=\s)', text)
job_title_ar = job_title_match.group(1).strip() if job_title_match else ""

# Extract the religion
religion_match = re.search(r'(?<=الديانة\s)(.*?)(?=\s)', text)
religion_ar = religion_match.group(1).strip() if religion_match else ""

# Extract the nationality
nationality_match = re.search(r'(?<=الجنسية\s)(.*?)(?=\s)', text)
nationality_ar = nationality_match.group(1).strip() if nationality_match else ""

# Extract the employer (صاحب العمل)
employer_match = re.search(r'(?<=صاحب العمل\s)([\u0621-\u064A\s]+)', text)
employer_ar = employer_match.group(1).strip() if employer_match else ""

# Translate Arabic fields to English
translator = Translator()

def translate(text):
    return translator.translate(text, src='ar', dest='en').text if text else ""

issue_place_en = translate(issue_place_ar)
job_title_en = translate(job_title_ar)
religion_en = translate(religion_ar)
nationality_en = translate(nationality_ar)
employer_en = translate(employer_ar)

# Prepare data for saving to Excel
data = {
    "Field": ["Name", "ID Number", "Issue Place", "Birth Date (Hijri)", "Expiry Date (Hijri)", "Job Title", "Religion", "Nationality", "Employer"],
    "Arabic": [name, id_number, issue_place_ar, birth_date_ar, expiry_date_ar, job_title_ar, religion_ar, nationality_ar, employer_ar],
    "English": [name, convert_arabic_to_english(id_number), issue_place_en, birth_date_en, expiry_date_en, job_title_en, religion_en, nationality_en, employer_en]
}

df = pd.DataFrame(data)

# Display the details first in Arabic, then in English
print("IQAMA DETAILS (Arabic):")
for i in range(len(df)):
    print(f"{df['Field'][i]}: {df['Arabic'][i]}")

print("\nIQAMA DETAILS (English):")
for i in range(len(df)):
    print(f"{df['Field'][i]}: {df['English'][i]}")

# Save the data to Excel
output_path = "saudi_iqama_data.xlsx"
df.to_excel(output_path, index=False)

print(f"Data has been saved to {output_path}")
