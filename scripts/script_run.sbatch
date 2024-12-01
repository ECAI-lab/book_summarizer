#!/bin/bash

#SBATCH --mem=80G
#SBATCH -c 2
#SBATCH --gres=gpu:1
#SBATCH -p gpu-h100sxm
#SBATCH --output=../slurm/%j.out

. ../../venv/bin/activate

python summarize_book.py --bookname "Brian Christian, Tom Griffiths - Algorithms to Live By_ The Computer Science of Human Decisions-Henry Holt and Co. (2016)"