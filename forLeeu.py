#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Preprocessing Barleus Corpus for Tracer

import sys
import os
import re
import time
import csv
import xml.etree.ElementTree as ET

ROOT_PATH = 'Corpus'
out_fn = "Corpus_%s" % time.strftime('%Y%m%d_%H%M%S')
OUT_FILE = open(out_fn + '.txt', 'w')
fname = "NoNotesleeu.xml"
writer = csv.writer(OUT_FILE, delimiter='\t')

def process_text(p, text_id, text_type, sender, recipient, date, letter_id, lang):
    for note in p.findall('note'):
            p.remove(note)
    for xref in p.findall('xref'):
            p.remove(xref)
    clean = ET.tostring(p, encoding='utf-8', method="text").decode().strip()
    clean= re.sub((r'\n\s*|\s+'),' ',clean)
    writer.writerow((text_id, clean, text_type, sender, recipient, date, letter_id, lang))


def process_artifact(el, out_file=OUT_FILE):

    lang = ''
    sender = ''
    recipient = ''
    letter_id = ''
    date = ''
    text_type =''
    text_id = 0


    for interp in el.findall('interpGrp/interp'):
        if 'type' in interp.attrib:
            interptype = interp.attrib['type']
        if 'value' in interp.attrib:
            value = interp.attrib['value']

            if interptype == 'id':
                letter_id += value
            if interptype == 'sender':
                sender += value
            if interptype == 'date':
                date += value
            if interptype == 'recipient':
                recipient += value
    for div in el.findall('div[@type="letter-page"]'):
        if 'lang' in div.attrib:
            lang = div.attrib['lang']
        for p in div.findall('p'):
            text_type = "body"
            print(text_type)
            print(p.text)
            process_text(p, text_id, text_type, sender, recipient, date, letter_id, lang)

    # in Huygens' corpus has to be just 'p'
    for p in el.findall('div[@type="letter-page"]/p'):
        for note in p.findall('note'):
            p.remove(note)
        for xref in p.findall('xref'):
            p.remove(xref)
        clean = ET.tostring(p, encoding='utf-8', method="text").decode().strip()
        clean= re.sub((r'\n\s*|\s+'),' ',clean)
    for div in el.findall('div[@type="letter-page"]/div'):
        print("found subdiv")
        if 'type' in div.attrib:
            text_type = div.attrib['type']
            print(text_type)

            for p in div.findall('p'):
                process_text(p, text_id, text_type, sender, recipient, date, letter_id, lang)


        # isolate punctuations?
        # add ID per sentence
        #sentences = re.split('(a-z|A-Z)(2)\.\s',clean)#I changed in order to avoid splitting on dots which do not end sentences
        #sentences = clean.split('. ')
        #for s in sentences:
        #out_file.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(clean, sender, recipient, date, lang))


def process_xml(fname):
    print ('Reading ' + fname)
    try:
        input_tree = ET.parse(fname)
        print("et.parsing:%s" % fname)
    except ET.ParseError:
        print ('Skipping ' + fname)
        return
    input_root = input_tree.getroot()
    elements = input_root.findall('TEI.2/text/body/div[@subtype="artifact"]')
    for input_el in elements:
        process_artifact(input_el)


def main(argv=None):
    if argv is None:
        argv = sys.argv
        args = argv[1:]
        for arg in args:
            if os.path.exists(arg):
                process_xml(arg)
                print("processin")
    else:
        # argv is a list of files
        for arg in argv:
            if os.path.exists(arg):
                print("processin " + arg)
                process_xml(arg)


if __name__ == "__main__":
    main([fname])
    OUT_FILE.close()
