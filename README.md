# Chill Your Bill

I created this script to redact information from my phone
bill as I submit expense reports. Only my personal phone
is allowed and not my families or other gadgets (watches).

This works for my ATT phone bill and makes a ton of assumptions
about the layout. Feel free to take any code from here or if 
you are feeling generous and know of a better way to do this
using Python feel free to let me know =).

## Project setup and run
I built this project on my Macbook. Its just some basic python setup.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python chill.py /path/to/att/bill.pdf -p 555.555.5555 -o /path/to/output.pdf
---

