# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Rocco DiVerdi
"""
# you may find it useful to import these variables
    #(although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq


def shuffle_string(s):
    """
    Shuffles the characters in the input string
    NOTE: this is a helper function, you do not have to modify this in any way
    """
    return ''.join(random.sample(s, len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """
    Returns the complementary nucleotide

    nucleotide: a nucleotide (A, C, G, or T) represented as a string
    returns: the complementary nucleotide

    Test all 4 possible nucleotides
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('T')
    'A'
    >>> get_complement('G')
    'C'
    """
    DNAcomplements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return DNAcomplements[nucleotide]


def get_reverse_complement(dna):
    """
    Computes the reverse complementary sequence of DNA for the specfied DNA
    sequence

    dna: a DNA sequence represented as a string
    returns: the reverse complementary DNA sequence represented as a string

    test some sequences:
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'

    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'

    test empty string, expect empty string:
    >>> get_reverse_complement('')
    ''
    """
    revComp = ''
    for i in range(len(dna)):
        revComp += get_complement(dna[-i-1])
    return revComp


def rest_of_ORF(dna):
    """
    Takes a DNA sequence that is assumed to begin with a start codon and
    returns the sequence up to but not including the first in frame stop
    codon.  If there is no in frame stop codon, returns the whole string.

    dna: a DNA sequence
    returns: the open reading frame represented as a string

    test sequences with stop codons in frame
    >>> rest_of_ORF("ATGTGAA")
    'ATG'

    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'

    test sequence with stop codons out of frame
    >>> rest_of_ORF("ATGAAGGTAGTTTAGAGAG")
    'ATGAAGGTAGTT'

    test sequence with no stop codons with multiple of 3 AAs
    >>> rest_of_ORF('ATGATGATGATG')
    'ATGATGATGATG'

    test sequence with no stop codons and a non-multiple of 3 # of AAs
    >>> rest_of_ORF('ATGAG')
    'ATGAG'

    test if '' is returned when '' is input
    >>> rest_of_ORF('')
    ''
    """
    ReadSequence = ''
    stop_codons = ['TAG', 'TGA', 'TAA']
    for i in range(0, len(dna), 3):
        if dna[i:i+3] in stop_codons:
            return dna[:i]
    return dna


def find_all_ORFs_oneframe(dna):
    """
    Finds all non-nested open reading frames in the given DNA sequence and
    returns them as a list.  This function should only find ORFs that are in
    the default frame of the sequence (i.e. they start on indices that are
    multiples of 3). By non-nested we mean that if an ORF occurs entirely
    within another ORF, it should not be included in the returned list of ORFs

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    test finding two sequential ORFs, ignoring ORFs in other reading frames
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    test for ignoring nested reading frames and skipping AAs outside of ORFs
     >>> find_all_ORFs_oneframe("ATGCTAATGAATGTAGACTAGCACATGTGCCC")
     ['ATGCTAATGAATGTAGAC', 'ATGTGCCC']

    test if [] is output if no ORFs are input
    >>> find_all_ORFs_oneframe('CGCGCCGGCCCCGGCGC')
    []
    """
    ORFs = []
    i = 0
    while i < len(dna):
        if dna[i:i+3] == 'ATG':
            ORF = rest_of_ORF(dna[i:])
            ORFs.append(ORF)
            i += len(ORF)
        i += 3
    return ORFs


def find_all_ORFs(dna):
    """
    Finds all non-nested open reading frames in the given DNA sequence in all
    3 possible frames and returns them as a list.  By non-nested we mean that
    if an ORF occurs entirely within another ORF and they are both in the same
    frame, it should not be included in the returned list of ORFs.

    dna: a DNA sequence
    returns: a list of non-nested ORFs

    test with an ORF in all three reading frames
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']

    test if [] is output when no ORFs are input
    >> find_all_ORFs("CGCCGGGCGCGCCCGCGGGC")
    []
    """
    allTheORFs = []
    for i in range(3):
        theseORFs = find_all_ORFs_oneframe(dna[i:])
        allTheORFs = allTheORFs + theseORFs
    return allTheORFs


def find_all_ORFs_both_strands(dna):
    """
    Finds all non-nested open reading frames in the given DNA sequence on both
    strands.

    dna: a DNA sequence
    returns: a list of non-nested ORFs

    test an orf on each strand
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']

    test if [] is returned when no ORFs are input
    >>> find_all_ORFs_both_strands('CGCCGCCGCGCGCGGCGCG')
    []
    """
    main_strand = dna
    comp_strand = get_reverse_complement(dna)

    return find_all_ORFs(main_strand) + find_all_ORFs(comp_strand)


def longest_ORF(dna):
    """
    Finds the longest ORF on both strands of the specified DNA and returns it
    as a string

    test to find the longest ORF on a string with multiple ORFs
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'

    test to return '' when '' is input
    >>> longest_ORF("")
    ''
    """
    ORFs = find_all_ORFs_both_strands(dna)
    if ORFs == []:
        return ''
    return max(ORFs, key=len)


def longest_ORF_noncoding(dna, num_trials):
    """
    Computes the maximum length of the longest ORF over num_trials shuffles
    of the specfied DNA sequence

    dna: a DNA sequence
    num_trials: the number of random shuffles
    returns: the maximum length longest ORF

        Test that there will be no ORFs in a list with no Ts
        >>> longest_ORF_noncoding('AGACCGACCAGACAACG',5)
        ''

        test that there will be no ORFs if num_trials = 0
        >>> longest_ORF_noncoding('ATG',0)
        ''
        """
    if num_trials == 0:
        return ''
    ORFs = []
    for i in range(num_trials):
        ORFs.append(longest_ORF(shuffle_string(dna)))
    return max(ORFs, key=len)


def coding_strand_to_AA(dna):
    """
    Computes the Protein encoded by a sequence of DNA.  This function
    does not check for start and stop codons (it assumes that the input
    DNA sequence represents a protein coding region).

    dna: a DNA sequence represented as a string
    returns: a string containing the sequence of amino acids encoded by the
             the input DNA fragment

        test for correct output given a coding ORF
        >>> coding_strand_to_AA("ATGCGA")
        'MR'

        test for correct output if the input doesn't have a multiple of 3 AAs
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'

        test if [] is returned when '' input
        >>> coding_strand_to_AA('')
        ''
    """
    AAs = ''
    for i in range(3, len(dna)+1, 3):
        AAs += aa_table[dna[i-3:i]]
    return AAs


def gene_finder(dna):
    """
    Returns the amino acid sequences coded by all genes that have an ORF
    larger than the specified threshold.

    dna: a DNA sequence
    threshold: the minimum length of the ORF for it to be considered a valid
       gene.
    returns: a list of all amino acid sequences whose ORFs meet the minimum
     length specified.

        test for a correct output (test may fail unless random_trials = 0)
        gene_finder("ATGCCCGCTTT")
        ['MPA']
    """
    random_trials = 1500
    threshold = len(longest_ORF_noncoding(dna, random_trials))

    AllOrfs = find_all_ORFs_both_strands(dna)
    Proteins = []
    for i in AllOrfs:
        if len(i) > threshold:
            Proteins.append(coding_strand_to_AA(i))
    return Proteins


def run_doctest():
    import doctest
    doctest.testmod()


def find_salmonella_gene():
    dna = load_seq("./data/X73525.fa")
    print gene_finder(dna)


if __name__ == "__main__":
    run_doctest()
    find_salmonella_gene()