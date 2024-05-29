import argparse
from Bio import SeqIO


def split_fasta_file(input_file, output_prefix, max_sequences=100):
    records = list(SeqIO.parse(input_file, "fasta"))
    num_sequences = len(records)
    num_files = (num_sequences + max_sequences - 1) // max_sequences

    for i in range(num_files):
        start = i * max_sequences
        end = min((i + 1) * max_sequences, num_sequences)
        output_file = f"{output_prefix}_{i}.fasta"
        SeqIO.write(records[start:end], output_file, "fasta")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to the input fasta file")
    parser.add_argument(
        "-n",
        "--max_sequences",
        type=int,
        default=100,
        help="Maximum number of sequences per output file",
    )
    args = parser.parse_args()

    out_prefix = args.input_file.split(".")[0]
    split_fasta_file(args.input_file, out_prefix, args.max_sequences)
