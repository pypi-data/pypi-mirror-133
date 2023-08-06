# cython: profile=False
# cython: embedsignature=True

from pysam.libcalignmentfile cimport AlignmentFile
from pysam.libcsamfile cimport Samfile
from pysam.libcfaidx cimport FastaFile
from pysam.libcalignedsegment cimport PileupColumn,PileupRead,pysam_bam_get_seq
from pysam.libchtslib cimport bam1_t, bam_pileup1_t
from libc.stdint cimport uint32_t, uint8_t, uint64_t, int64_t
from cpython cimport PyBytes_FromStringAndSize

cdef char* bam_nt16_rev_table = "=ACMGRSVTWYHKDBN"



cdef inline object get_seq_base(bam1_t *src, uint32_t k):
    cdef uint8_t* p
    cdef char* s

    if not src.core.l_qseq:
        return None

    seq = PyBytes_FromStringAndSize(NULL, 1)
    s   = <char*>seq
    p   = pysam_bam_get_seq(src)

    s[0] = bam_nt16_rev_table[p[k//2] >> 4 * (1 - k%2) & 0xf]

    return seq

def allbase(FastaFile fafile,str chrom,int reference_length,dict rec_lst):
    cdef:
        int position
        str refbase
    for position in range(reference_length):
        if position not in rec_lst:
            rec = {'Pos':None,'A':0,'C':0,'G':0,'T':0,'N':0,'DEL':0,'INS':0,'Ref':None,'Depth':0}
            refbase = fafile.fetch(reference=chrom, start=position, end=position+1).upper()
            rec['Pos'] = position+1 #zero-based to one-based
            rec['Ref'] = refbase  
            rec_lst[position] = rec
  

def count_bases(str bamFile,str reference,bint truncate=False,int min_mapping_quality=0,int min_base_quality=0,str stepper='nofilter'):
    cdef:
        FastaFile fafile = FastaFile(reference)
        str chrom = fafile.references[0]
        int reference_length = fafile.lengths[0]
        AlignmentFile alignmentfile = AlignmentFile(bamFile)
        PileupColumn pc 
        dict rec_lst={}
        str refbase
        bytes alnbase
        int i,n,position
        bam_pileup1_t** plp
        bam_pileup1_t* read
    pp = alignmentfile.pileup(max_depth=20000,stepper=stepper,truncate=truncate,min_mapping_quality=min_mapping_quality,min_base_quality=min_base_quality)
    for pc in pp:
        rec = {'Pos':None,'A':0,'C':0,'G':0,'T':0,'N':0,'DEL':0,'INS':0,'Ref':None,'Depth':0}
        n = pc.get_num_aligned()
        plp = pc.plp
        position = pc.pos
        rec['Depth'] = n
        refbase = fafile.fetch(reference=chrom, start=position, end=position+1).upper()
        rec['Pos'] = position+1 #zero-based to one-based
        rec['Ref'] = refbase 
        for i in range(n):
            read = &(plp[0][i])
            if read.is_del:
                if not read.is_refskip:
                    rec['DEL'] += 1
            else:
                alnbase = get_seq_base(read.b, read.qpos)
                if alnbase == b'A':
                    rec['A'] += 1
                elif alnbase == b'T':
                    rec['T'] += 1
                elif alnbase == b'C':
                    rec['C'] += 1
                elif alnbase == b'G':
                    rec['G'] += 1
                elif alnbase == b'N':
                    rec['N'] += 1
                if read.indel > 0:
                    rec['INS'] += 1
        
        rec_lst[position]=rec
    allbase(fafile,chrom,reference_length,rec_lst)

    return rec_lst

