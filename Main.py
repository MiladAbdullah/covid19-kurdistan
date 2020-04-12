# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 22:37:34 2020

@author: Milad
"""

from Bio import Entrez

def find_seq(singleID):   #the singleID is the accession number
    handle = Entrez.efetch(db='nucleotide',id=singleID, rettype = 'fasta', retmode= 'text')
    f = open('%s.fasta' % singleID, 'w')
    f.write(handle.read())
    handle.close()
    f.close()