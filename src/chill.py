import fitz
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("input")
parser.add_argument("-o", "--output")
parser.add_argument("-p", "--phone")
parser.add_argument("-n", "--name")

args = parser.parse_args()
input = args.input
output = args.output
phone = args.phone
name = args.name

doc = fitz.open(input)

prev_phone_number = ""
for page in doc.pages():

    wlist = page.get_text("words", delimiters=None, sort=True)
    for i,w in enumerate(wlist):
        page_bound = page.bound()
        box = page.get_textbox((page_bound[0], w[1], page_bound[2], w[3]))

        if "Phone," in w[4] or "Wearable," in w[4]:
            prev_phone_number = wlist[i+1][4]

        if ("$" in w[4] and 
                (name not in box and (prev_phone_number != phone or w[0] > page.rect[2] * .65 ))):
            page.add_redact_annot(w[:4], fill=(0,0,0))

    page.apply_redactions()

doc.save(output)
doc.close()
