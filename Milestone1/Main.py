import json
import os
from youtube_transcript_api import YouTubeTranscriptApi


def vid_id(url):
   
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    else:
        print("Error: Invalid YouTube URL")
        return None


def sweep_txt(text):
   
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def fetch_transcript(url):
 
    # Get video ID
    video_id = vid_id(url)
    if not video_id:
        return


    os.makedirs("outputs", exist_ok=True)

   
    
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
    except Exception as e:
        print(f"fuck: {e}")
        return

    # Process transcript segments
    full_text = []
    structured_data = []

    for segment in transcript:
        cleaned = sweep_txt(segment.text)
        if cleaned:
            full_text.append(cleaned)
            structured_data.append({
                "text": cleaned,
                "start": segment.start,
                "duration": segment.duration
            })


    txt_path = f"outputs/{video_id}.txt"
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(" ".join(full_text))

    json_path = f"outputs/{video_id}.json"
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=2, ensure_ascii=False)

    print(f"\n✓ Transcript saved successfully!")
    print(f"  - Text file: {txt_path}")
    print(f"  - JSON file: {json_path}")
    print(f"  - Video ID: {video_id}")




print("YouTube Transcript Downloader - Milestone 1")

video_url = input("\nEnter YouTube URL: ")
fetch_transcript(video_url)
