import json
import os
from transformers import pipeline


print("Loading AI Model (BART)...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def create_chunks(text, chunk_size=1200, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
      
        start += (chunk_size - overlap)
    return chunks

def run_summarization():
   
    video_id = input("Enter the Video ID (e.g., dQw4w9WgXcQ): ")
    input_path = f"outputs/{video_id}.txt"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run your first script first!")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        full_text = f.read()

  
    print(f"Splitting text into overlapping chunks...")
    chunks = create_chunks(full_text)


    print(f"Summarizing {len(chunks)} segments...")
    intermediate_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  Processing chunk {i+1}/{len(chunks)}...")
        # Summarize the chunk
        res = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        intermediate_summaries.append(res[0]['summary_text'])

    
  
    combined_text = " ".join(intermediate_summaries)
    
 
    final_summary = summarizer(combined_text[:2000], max_length=300, min_length=10)[0]['summary_text']

    # Save the final result
    output_path = f"outputs/{video_id}_SUMMARY.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"summary saved to: {output_path}")

if __name__ == "__main__":
    run_summarization()

