import json
import os
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):
    """Get the video ID from a YouTube URL"""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    else:
        print("Error: Invalid YouTube URL")
        return None


def clean_text(text):
    """Clean transcript text - remove line breaks and extra spaces"""
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def download_transcript(url):
    """Download and save YouTube video transcript"""
    # Get video ID
    video_id = get_video_id(url)
    if not video_id:
        return

    # Create outputs folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)

    # Get transcript using fetch method
    print("Downloading transcript...")
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
    except Exception as e:
        print(f"Error downloading transcript: {e}")
        return

    # Process transcript segments
    full_text = []
    structured_data = []

    for segment in transcript:
        cleaned = clean_text(segment.text)
        if cleaned:
            full_text.append(cleaned)
            structured_data.append({
                "text": cleaned,
                "start": segment.start,
                "duration": segment.duration
            })

    # Save as TXT file
    txt_path = f"outputs/{video_id}.txt"
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(" ".join(full_text))

    # Save as JSON file
    json_path = f"outputs/{video_id}.json"
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=2, ensure_ascii=False)

    print(f"\n✓ Transcript saved successfully!")
    print(f"  - Text file: {txt_path}")
    print(f"  - JSON file: {json_path}")
    print(f"  - Video ID: {video_id}")


# Main program
print("=" * 50)
print("YouTube Transcript Downloader - Milestone 1")
print("=" * 50)
video_url = input("\nEnter YouTube URL: ")
download_transcript(video_url)
print("\n" + "=" * 50)