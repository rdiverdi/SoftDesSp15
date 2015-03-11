class DNASequence(object):
    """ Represents a sequence of DNA """
    def __init__(self, nucleotides):
        """ constructs a DNASequence with the specified nucleotides.
             nucleotides: the nucleotides represented as a string of
                          capital letters consisting of A's, C's, G's, and T's """
        self.nucleotides = nucleotides
        pass

    def __str__(self):
        """ Returns a string containing the nucleotides in the DNASequence
        >>> seq = DNASequence("TTTGCC")
        >>> print seq
        TTTGCC
        """
        return self.nucleotides
        pass

    def get_reverse_complement(self):
        """ Returns the reverse complement DNA sequence represented
            as an object of type DNASequence

            >>> seq = DNASequence("ATGC")
            >>> rev = seq.get_reverse_complement()
            >>> print rev
            GCAT
            >>> print type(rev)
            <class '__main__.DNASequence'>
        """
        complements = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
        rev_comp = ''
        for nucleotide in str(self):
            rev_comp = complements[nucleotide] + rev_comp
        return DNASequence(rev_comp)
        pass

    def get_proportion_ACGT(self):
        """ Computes the proportion of nucleotides in the DNA sequence
            that are 'A', 'C', 'G', and 'T'
            returns: a dictionary where each key is a nucleotide and the
                corresponding value is the proportion of nucleotides in the
            DNA sequence that are that nucleotide.
            (NOTE: this doctest will not necessarily always pass due to key
                    re-ordering don't worry about matching the order)
        >>> seq = DNASequence("AAGAGCGCTA")
        >>> d = seq.get_proportion_ACGT()
        >>> print (d['A'], d['C'], d['G'], d['T'])
        (0.4, 0.2, 0.3, 0.1)
        """
        seq = str(self)
        d = {
             'A':seq.count('A')/float(len(seq)),
             'C':seq.count('C')/float(len(seq)),
             'G':seq.count('G')/float(len(seq)),
             'T':seq.count('T')/float(len(seq))
             }
        return d
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
