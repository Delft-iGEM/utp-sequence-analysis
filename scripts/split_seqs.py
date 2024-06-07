import argparse
from pathlib import Path
from Bio import SeqIO


def split_fasta_file(input_file, output_prefix, out_dir=".", max_sequences=100):
    out_dir = Path(out_dir)
    records = list(SeqIO.parse(input_file, "fasta"))
    num_sequences = len(records)
    num_files = (num_sequences + max_sequences - 1) // max_sequences

    for i in range(num_files):
        start = i * max_sequences
        end = min((i + 1) * max_sequences, num_sequences)
        if num_files == num_sequences:
            output_file = records[i].id + ".fasta"
        else:
            output_file = f"{output_prefix}_{i}.fasta"
        file_path = out_dir / output_file
        SeqIO.write(records[start:end], file_path, "fasta")


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
    parser.add_argument(
        "--out-dir",
        help="Output directory for the split fasta files",
        default=".",
    )
    args = parser.parse_args()

    out_prefix = Path(args.input_file).stem
    split_fasta_file(args.input_file, out_prefix, args.out_dir, args.max_sequences)
