import argparse
from transformers import pipeline 
import torch
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from tqdm import tqdm 

from slack_webhook import post_via_webhook


# Define function to parse the EPUB file
def extract_chapters_from_epub(file_path):
    book = epub.read_epub(file_path)
    chapters = []
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text()
            chapters.append(text)
    return chapters


def query_llm(pipeline, prompt):
    messages = [
        {"role": "user", "content": prompt},
    ]
    return pipeline(messages)[0]["generated_text"][-1]["content"]


def summarize_book(args):
    # Prepare text generation pipeline
    pipe = pipeline(
        "text-generation", 
        model=args.model, 
        torch_dtype=torch.float16,
        device=0,
        max_new_tokens=2048
    )

    # File path to the EPUB file
    epub_file_path = f"../eBooks/{args.bookname}.epub"
    chapters = extract_chapters_from_epub(epub_file_path)
    print(f"bookname: {args.bookname}, num chapters: {len(chapters)}")

    # Summarize each chapter and save summaries to a file
    sep = "\n---\n"
    target_fn = f"../eBooks/{args.bookname}_summary-{args.model_shortname}-truncation.md"
    
    # For very short "chapters", put them into the buffer. 
    # For very long "chapters", truncate the first MAX_PROMPT_CHAR_COUNT characters.
    chapter_buff = " "
    for chapter in tqdm(chapters):
        if len(chapter) < 50:
            chapter_buff = chapter_buff + "\n" + chapter
            continue  
        else:
            chapter_buff = chapter_buff + "\n" + chapter
            print("Debug: chapter character len:", len(chapter_buff))
            MAX_PROMPT_CHAR_COUNT = 40000
            while len(chapter_buff) > MAX_PROMPT_CHAR_COUNT:
                summary = query_llm(pipe, f"Summarize a chapter and write out the summary in markdown format in English. Start by listing the chapter number and the title of the chapter in large font. This might be a partial chapter due to truncation, so don't worry if the chapter title can't be found, and just do your best at summarizing the text. I'm particularly interested in the characters mentioned in the chapter, their thought processes, and how their decisions led to the outcomes. Following is the content for summary:\n {chapter_buff[:MAX_PROMPT_CHAR_COUNT]}")
                chapter_buff = chapter_buff[MAX_PROMPT_CHAR_COUNT:]
                with open(target_fn, "a+") as f:
                    f.write(f"{summary}\n{sep}\n")
            chapter_buff = " "

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bookname", type=str, help="The filename of the epub book. Do NOT include the extension, i.e., .epub.")
    parser.add_argument("--model", type=str, default="Qwen/QwQ-32B-Preview", help="This is the model name on Huggingface model hub")
    parser.add_argument("--model_shortname", type=str, default="QwQ", help="This is a shortname used to label the file. Do NOT include slash in the shortname.")
    args = parser.parse_args()
    summarize_book(args)
    post_via_webhook("Book {} summarization via {} done!".format(args.bookname, args.model_shortname))