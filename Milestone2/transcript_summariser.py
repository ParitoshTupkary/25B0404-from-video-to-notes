import json
import os
from transformers import pipeline

# 1. Setup the AI Model (Milestone 3)
print("Loading AI Model (BART)...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def create_chunks(text, chunk_size=1200, overlap=150):
    """Milestone 2: Creating overlapping chunks exactly as the guide says"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # Move forward but keep 150 characters of overlap for context
        start += (chunk_size - overlap)
    return chunks

def run_summarization():
    # Ask for the video ID (the filename in your outputs folder)
    video_id = input("Enter the Video ID (e.g., dQw4w9WgXcQ): ")
    input_path = f"outputs/{video_id}.txt"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run your first script first!")
        return

    # Read the text your gospel script saved
    with open(input_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Step A: Chunking (Milestone 2)
    print(f"Splitting text into overlapping chunks...")
    chunks = create_chunks(full_text)

    # Step B: Summarize each segment (Milestone 3)
    print(f"Summarizing {len(chunks)} segments...")
    intermediate_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  Processing chunk {i+1}/{len(chunks)}...")
        # Summarize the chunk
        res = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        intermediate_summaries.append(res[0]['summary_text'])

    # Step C: Final Summary of Summaries (Hierarchical Strategy)
    print("Combining summaries into final result...")
    combined_text = " ".join(intermediate_summaries)
    
    # One final pass to get the core message
    final_summary = summarizer(combined_text[:2000], max_length=300, min_length=100)[0]['summary_text']

    # Save the final result
    output_path = f"outputs/{video_id}_SUMMARY.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"\n✓ DONE!")
    print(f"Final summary saved to: {output_path}")

if __name__ == "__main__":
    run_summarization()
