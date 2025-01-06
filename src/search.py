
import pandas as pd

def search_in_excel(std_code):

    # Load the Excel file
    file_path = 'd.xlsx'  # Replace with your file path
    sheet_name = 'sheet1'  # Replace with your sheet name if different
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Filter rows based on conditions
    filtered_rows = df[(df['شماره دانشجویی'] == std_code)]
    # print(filtered_rows[['ردیف', 'نام', 'نام‌خانوادگی', 'شماره دانشجویی', 'کد تخفیف']])
    # Print the filtered rows
    if not filtered_rows.empty:
        # print(filtered_rows[['نقد جهت عقد قرارداد', 'مبلغ قسط هر ماه', 'تعداد خواب']])
        res = filtered_rows[['ردیف', 'نام', 'نام‌خانوادگی', 'شماره دانشجویی', 'کد تخفیف']]
    else:
        res = None

    return res

def convert_numbers(text: str) -> str:
    persian_to_arabic = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }
    for p_digit, e_digit in persian_to_arabic.items():
        text = text.replace(p_digit, e_digit)
    return text
