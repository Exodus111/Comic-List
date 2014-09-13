#! /usr/bin/env python

text = open("Marvel_Comics.txt", "r").read()

def text_fix(text):
    text = text.strip("{[]}")
    text = text.strip()
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.replace(",","\n")
    return text

def make_textfile(text):
    output = open("out_file.txt", "w")
    mylist = []
    text = text_fix(text)
    for line in text.splitlines():
        mylist.append(line)

    mylist.sort()
    for i in mylist:
        i = i.lstrip()
        output.write(i)
        output.write("\n")

make_textfile(text)
