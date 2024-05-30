#!/usr/bin/python3
"""

Usage: ProtT5-XL-U50-embedding.py <input fasta file>'

"""

from pathlib import Path
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import os
import sys
import re
import argparse
from tqdm import tqdm
from datetime import datetime
from Bio import SeqIO
import torch
from transformers import T5EncoderModel, T5Tokenizer
import gc
import h5py


def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print(
            "\n Time taken: %i hours %i minutes and %s seconds."
            % (thour, tmin, round(tsec, 2))
        )


parser = argparse.ArgumentParser(
    description="\n Calculate ProtT5-XL-U50 1024 vector representations for FASTA sequences.\n",
    epilog="\n \n",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("sequences", help="path to the FASTA file")
parser.add_argument(
    "-mean",
    dest="mean_vec",
    help="calculaate single vector per sequence [default: calculate per residue]",
    action="store_true",
    default=False,
    required=False,
)
parser.add_argument(
    "-nogpu",
    dest="usegpu",
    help="do not use GPU [default: use if available]",
    action="store_false",
    default=True,
    required=False,
)
parser.add_argument(
    "-out",
    dest="out",
    help="path to output h5 file [default: ./embeddings.h5]",
    default="./embeddings.h5",
    required=False,
)

args = parser.parse_args()

if os.access(args.sequences, os.R_OK):

    FastaFile = open(args.sequences, "r")
    nseq = 0
    for line in FastaFile:
        if line.startswith(">"):
            nseq += 1
    FastaFile.close()

    start_time = timer(None)
    stripped = os.path.splitext(args.sequences)[0]
    feats = 1024
    features = []
    for i in range(feats):
        features += ["vector_" + str("%04d" % (i + 1))]
    #    print(features)

    # Load the vocabulary and ProtT5-XL-UniRef50 Model
    tokenizer = T5Tokenizer.from_pretrained(
        "Rostlab/prot_t5_xl_uniref50", do_lower_case=False
    )
    model = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_uniref50")
    gc.collect()

    # Load the model into the GPU if avilabile and switch to inference mode
    if args.usegpu:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device("cpu")
    model = model.to(device)
    model = model.eval()

    outfile = Path(args.out)
    fasta_sequences = SeqIO.parse(args.sequences, "fasta")
    with h5py.File(outfile, "w") as f:
        with tqdm(total=nseq, desc="  Embedding", ncols=150, mininterval=5) as pbar:
            for fasta in fasta_sequences:
                # for fasta in tqdm(fasta_sequences, desc='  Embedding', ncols=150, mininterval=2):
                sequences = []
                # name, seq = fasta.description.split(" ")[0], list(" ".join(str(fasta.seq)))
                name, seq = fasta.id.split(" ")[0], str(fasta.seq)
                # delete * signs prodigal puts at the end of sequence
                seq = re.sub(r"\*", "", seq)
                slen = len(seq)
                #            sequences.append(" ".join(str(fasta.seq)))
                sequences.append(" ".join(seq))
                name = re.sub(r"\|", "_", name)
                name = re.sub(r"\/", "_", name)
                # map rarely occured amino acids (U,Z,O,B) to (X)
                sequences = [
                    re.sub(r"[UZOJB]", "X", sequence) for sequence in sequences
                ]
                # Tokenize, encode sequences and load it into the GPU if possibile
                ids = tokenizer.batch_encode_plus(
                    sequences, add_special_tokens=True, padding=True
                )
                input_ids = torch.tensor(ids["input_ids"]).to(device)
                attention_mask = torch.tensor(ids["attention_mask"]).to(device)
                # Extracting sequence features and load it into the CPU if needed
                with torch.no_grad():
                    embedding = model(
                        input_ids=input_ids, attention_mask=attention_mask
                    )
                embedding = embedding.last_hidden_state.cpu().numpy()
                # Remove padding (\<pad>) and special tokens (\</s>) that is added by ProtT5-XL-UniRef50 model
                features = []
                for seq_num in range(len(embedding)):
                    seq_len = (attention_mask[seq_num] == 1).sum()
                    seq_emd = embedding[seq_num][: seq_len - 1]
                    features.append(seq_emd)

                # df = pd.DataFrame(data=np.array(features).flatten().reshape(slen,1024), columns=features)
                features = np.array(features).astype(float).reshape(slen, 1024)
                if args.mean_vec:
                    # df = pd.DataFrame(
                    #     np.array(features).astype(float).reshape(slen, 1024).mean(axis=0)
                    # )
                    # df = df.transpose(copy=True)
                    features = features.mean(axis=0)
                f.create_dataset(name, data=features)

                pbar.update()

    timer(start_time)

else:
    parser.error(
        '\n !!! Input file "%s" does not exist in this directory !!!\n' % args.sequences
    )
