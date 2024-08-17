# Script to redact all of my ATT phone bill items exept ones that apply to my own Phone
# This is because I can only expense my phone bill and not my watch or any dependents. 

import fitz
import re
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("input")
parser.add_argument("-o", "--output")
parser.add_argument("-p", "--phone")

args = parser.parse_args()
input = args.input
output = args.output
phone = args.phone

doc = fitz.open(input)

prev_phone_number = ""
for page in doc.pages():

    word_list = page.get_text("words", delimiters=None, sort=True)
    for w in word_list:
        word = w[4]
        page_bounds = page.bound()
        page_line_for_word = page.get_textbox((page_bounds[0], w[1], page_bounds[2], w[3]))

        # Simple way to track when to start and stop redacting dollar values. 
        # Some assumptions are made here that the phone number is not the last number in the wireless table. 
        # If it was the last number then some of the totals may be shown.
        phone_regex = re.compile(r"\d{3}\.\d{3}\.\d{4}")
        if phone_regex.match(word):
            prev_phone_number = word

        # There are some tables on the right side of the page that are interlieved with bill values that
        # I don't want redacted. Luckily all dollar values on the righ side of the page always need to be redacted.
        word_left_x = w[0]
        page_width = page.rect[2]
        if ("$" in word 
            and phone not in page_line_for_word  #covers the case for the first "simplified" table for the bill
            and (prev_phone_number != phone or word_left_x > page_width * .65 )): #covers the itemized list of my phone bill plus the right side of the page
            page.add_redact_annot(w[:4], fill=(0,0,0))

    page.apply_redactions()

doc.save(output)
doc.close()
