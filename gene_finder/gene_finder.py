# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Rocco DiVerdi

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    DNAcomplements = {'A':'T','T':'A','C':'G','G':'C'}
    return DNAcomplements[nucleotide]

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    revComp = ''
    for i in range(len(dna)):
        revComp += get_complement(dna[-i-1])
    return revComp

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    ReadSequence = ''
    for i in range(0, len(dna), 3):
        stop_codons = ['TAG', 'TGA', 'TAA']
        if dna[i:i+3] in stop_codons:
            return dna[0:i]
    return dna

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    ORFs = []
    i = 0
    while i < len(dna):
        if dna[i:i+3] == 'ATG':
            ORF = rest_of_ORF(dna[i:len(dna)])
            ORFs.append(ORF)
            i += len(ORF)
        i += 3
    return ORFs


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    allTheORFs = []
    for i in range(3):
        theseORFs = find_all_ORFs_oneframe(dna[i:len(dna)])
        allTheORFs = allTheORFs + theseORFs
    return allTheORFs


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    main_strand = dna
    comp_strand = get_reverse_complement(dna)

    return find_all_ORFs(main_strand) + find_all_ORFs(comp_strand)


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    >>> longest_ORF("")
    ''
    """
    ORFs = find_all_ORFs_both_strands(dna)
    if ORFs == []:
        return ''
    return max(ORFs, key=len)


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF

        Test that there will be no ORFs in a list with no Ts 
        >>> longest_ORF_noncoding('AGACCGACCAGACAACG',5)
        ''

        """

    ORFs = []
    for i in range(num_trials):
        ORFs.append(longest_ORF(shuffle_string(dna)))
    return max(ORFs, key=len)


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents a protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    AAs = ''
    for i in range(3,len(dna)+1,3):
        AAs += aa_table[dna[i-3:i]]
    return AAs

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.

        >>> gene_finder("ATGCCCGCTTT",7)
        ['MPA']
    """

    threshold = len(longest_ORF_noncoding(dna,2))

    AllOrfs = find_all_ORFs_both_strands(dna)
    Proteins = []
    for i in AllOrfs:
        if len(i) > threshold:
            Proteins.append(coding_strand_to_AA(i))
    return Proteins
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()