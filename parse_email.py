print("Hello world")

from email import message_from_string
import re
import os 
import csv

def extract(raw_email):
    msg = message_from_string(raw_email)
    if (msg.is_multipart()):
        return msg.get_payload(0).get_payload()
    return msg.get_payload()

def normalize(extracted_email_body):

    replace_urls = re.sub(r'http\S+|www\S+', 'URL' ,extracted_email_body)

    remove_html = re.sub(r'<[^>]+>', ' ', replace_urls)

    remove_whitespace = re.sub(r'[\s+]',' ', remove_html)

    remove_puncuation = re.sub(r'[^\w\s]', ' ', remove_whitespace)

    replace_numbers = re.sub(r'\b\d+\b','NUMBER', remove_puncuation)

    final = replace_numbers

    clean_text = ' '.join(final.split())

    #print(f"cleaned_text: {clean_text}")

    return clean_text


def load_emails_from_dir(directory, label):

    data = []
    file_num = 0
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                file_num = file_num + 1
                raw_email = f.read()
                email_body = extract(raw_email)
                print(file_num)
                
                if not isinstance(email_body, str):
                    continue


                clean_text = normalize(email_body)
                data.append((clean_text, label))

        except Exception:
            continue        

    return data


spam = load_emails_from_dir(r"path_to_spam_directory_here", 1)
easy_ham = load_emails_from_dir(r"path_to_ham_directory_here",0)
hard_ham = load_emails_from_dir(r"path_to_hard_ham_directory_here",0)

data = spam + easy_ham
full_data = data + hard_ham


with open(r"path_to_csv_file", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Text', 'Label'])
    writer.writerows(full_data)








