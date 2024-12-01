# Book summarizer
Reads an epub format book. Use an LLM to summarize it chapter by chapter, and write it to output.

## Dependencies
1. Install the software packages.  
```
pip install EbookLib beautifulsoup4
pip install transformers torch
```

2. To allow Slack integration, set an incoming webhook URL and export it to the environment variable `SLACK_WEBHOOK_URL`. Otherwise, uncomment the line `post_via_webhook` in the main script `summarize_book.py`.  

## Usage
1. Place a book in the `eBooks` folder. Let's say the file name is `book_name.epub`.  
2. Enter the `scripts` folder.  
3. Call `sbatch script_run.sbatch` to launch the computation job to slurm.  
4. When the job completes, the resulting book summary (in markdown) will appear in `eBooks` folder as `book_name_summary-modelname.md`  

## Configurations
- To change the GPUs to run on, modify the `script_run.sbatch` script.  
- To change the model, modify the `--model` and `--model_shortname` when calling `summarize_book.py`.  
- To change the prompt, modify the command in the `summarize_book.py`  