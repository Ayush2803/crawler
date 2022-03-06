from cleantext import clean
import pandas as pd
import re


def remove_indexing(text):
    text = re.sub(' *\(?[A-Za-z0-9]\) *', '', text)
    return text


####### CLEAN THE DATA ##########
df = pd.read_csv('rawdata.csv')
clean_paras = []
clean_headings = []
for element in df['paras']:
    element = str(element)
    element = remove_indexing(element)
    clean_paras.append(clean(element,
                             fix_unicode=True,               # fix various unicode errors
                             to_ascii=True,                  # transliterate to closest ASCII representation
                             lower=False,                     # lowercase text
                             # fully strip line breaks as opposed to only normalizing them
                             no_line_breaks=False,
                             no_urls=True,                  # replace all URLs with a special token
                             no_emails=True,                # replace all email addresses with a special token
                             no_phone_numbers=True,         # replace all phone numbers with a special token
                             no_numbers=True,               # replace all numbers with a special token
                             no_digits=True,                # replace all digits with a special token
                             no_currency_symbols=True,      # replace all currency symbols with a special token
                             no_punct=True,                 # remove punctuations
                             replace_with_url=" ",
                             replace_with_email=" ",
                             replace_with_phone_number=" ",
                             replace_with_number=" ",
                             replace_with_digit=" ",
                             replace_with_currency_symbol=" ",
                             lang="en"                       # set to 'de' for German special handling
                             ))

############ CLEAN THE TITLES ###################################################

for element in df['headings']:
    element = str(element)
    element = remove_indexing(element)
    clean_headings.append(clean(element,
                                fix_unicode=True,               # fix various unicode errors
                                to_ascii=True,                  # transliterate to closest ASCII representation
                                lower=False,                     # lowercase text
                                # fully strip line breaks as opposed to only normalizing them
                                no_line_breaks=False,
                                no_urls=True,                  # replace all URLs with a special token
                                no_emails=True,                # replace all email addresses with a special token
                                no_phone_numbers=True,         # replace all phone numbers with a special token
                                no_numbers=True,               # replace all numbers with a special token
                                no_digits=True,                # replace all digits with a special token
                                no_currency_symbols=True,      # replace all currency symbols with a special token
                                no_punct=True,                 # remove punctuations
                                replace_with_url=" ",
                                replace_with_email=" ",
                                replace_with_phone_number=" ",
                                replace_with_number=" ",
                                replace_with_digit=" ",
                                replace_with_currency_symbol=" ",
                                lang="en"                       # set to 'de' for German special handling
                                ))

# Remove blank strings
while("" in clean_paras):
    clean_paras.remove("")

# Remove blank strings
while("" in clean_headings):
    clean_headings.remove("")

while("nan" in clean_headings):
    clean_headings.remove("nan")
while("nan" in clean_paras):
    clean_paras.remove("nan")

clean_sentences = pd.DataFrame(clean_paras)
clean_sentences.to_csv('paragraphs.csv')

clean_titles = pd.DataFrame(clean_headings)
clean_titles.to_csv('titles.csv')
