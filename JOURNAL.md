## Motif Discovery

1. UCYN-A enriched proteins were selected from `data/ADK1075_ProteinQuantifications.csv` (`clustering.ipynb`)
2. MSA was created from `data/ADK1075_proteomics_DB_2.fasta` using COBALT. (`ucyn-a_enriched/ucyn-a_enriched_cobalt.fa`)
3. The alignment was cleaned up using `CIAlign --remove-insertions` (`ucyn-a_enriched/ucyn-a_enriched_cobalt_cleaned.fa`)
4. Alignments with at least 60% coverage in the 880-1010 region were selected (`motifs.ipynb`, `ucyn-a_enriched/good-c-term.fasta`)
5. Gblocks was used to crop the selected alignments (`ucyn-a_enriched/good-c-term-gb.fasta`) Parameters:
   ```
   Minimum Number Of Sequences For A Conserved Position: . 104
   Minimum Number Of Sequences For A Flank Position: ..... 104
   Maximum Number Of Contiguous Nonconserved Positions: .. 15
   Minimum Length Of A Block: ............................ 10
   Allowed Gap Positions: ................................ All
   ```
6. MEME was run on the cropped aligments with `-protein -nmotifs 10 -neg ./proteomics_DB_no_c_term.fasta -objfun de` (`ucyn-a_enriched/meme/meme_gb.xml`)
7. The motifs were visualized in `motifs.ipynb`

## Transit Peptide Evaluation

## Transit Peptide
