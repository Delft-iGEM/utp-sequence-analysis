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

## Motif Analysis

1. The positions of each motif's each occurence was computed relative to motif_1, which occured in 184 out of 204 sequences (`motifs.ipynb`)
2. The distribution of these relative positions was visualized in `motifs.ipynb`
3. The different combinations of motifs and the distribution of relative positions of motifs within these combinations were also visualized in `motifs.ipynb`
4. The relationship between the mature domain and the motifs in the corresponding transit peptide was also analyzed:
   1. Embeddings using``prot_t5_xl_uniref50` were computed for each mature domain
   2. Several classifiers (`LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier`, `SVC` as implemented by sklearn, using default parameters) were trained to predict motif combinations based on protein mebeddings
   3. Another set of classifiers (`DecisionTreeClassifier`, `RandomForestClassifier`, `SVC` as implemented by sklearn, using default parameters) were trained to predict motif combinations from amino acid contents of the mature domain
   4. In both cases, binomial test was used to evaluate the statistical significance of the classifier accuracy, with `p < 0.05`

## Structure analysis

1. Structures for each UCYN-A imported protein selected in Motif Discovery (`ucyn-a_enriched/good-c-term-full.fasta`) was predicted using AlphaFold3 with default parameters.
2. The structure data was analyised using biopython.PDB (`structs.ipynb`)
3. The structure predictions were clustered
   1. The structures were pairwise superimposed using `Biopython.PDB.Superimposer` and the RMSD calculated for each pair
   2. These pairwise distances were used to create a hierarchical clustering using `scipy.cluster.hierarchy` (`structs.ipynb`)
4. For analyising the structure of the c-terminal regions, 49 structures with strong c-terminal sequence similarity were selected (`structs.ipynb`)
   1. These were structurally aligned using PyMOL's `cealign` command (`utp-data/align-c-term.pse`)
   2. The aligned structures were visualized in `structs.ipynb`
   3. The alignments were used to create a consensus structure (`structs.ipynb`, `results/consensus-c-term.pdb`)

## Protein Localization Prediction

1. The localization of each UCYN-A enriched protein was predicted using [MuLocDeep](https://www.mu-loc.org/) -> `ucyn-a_enriched/mulocdeep-localization`
2. The attention weights as a function of sequence postion were visualized in `localizations.ipynb`
3. The total C-terminal and N-terminal attention weights were compared for different localizations in `localizations.ipynb`

## Transit Peptide Evaluation

1. HMM profiles were created for the UCYN-A enriched proteins with significant C-terminal alignments (`utp-data/good-c-term-full.fasta`) using `hmmbuild` from HMMER
2. The prediction performance of the HMM profiles was evaluated by creating a positive and negative control datasets, the latter by sampling sequences from `data/ADK1075_proteomics_DB_2.fasta` with the same length distribution as the positive dataset. (`hmm.ipynb`)
3. The profile was then used to evaluate protein+transit peptide constructs.
4. The structure of folded protein+transit peptide constructs was aligned with the consensus structure using PyMol's `cealing` function

## Transit Peptide Homology Search
