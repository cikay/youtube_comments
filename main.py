import os
import json
import pandas as pd
from tqdm import tqdm
import subprocess
import time
import argparse

def get_comments_with_ytdlp(video_id, output_folder="comments"):
    """
    Download comments from a YouTube video using yt-dlp
    
    Args:
        video_id (str): YouTube video ID
        output_folder (str): Folder to save the comments
    
    Returns:
        list: List of comment dictionaries
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    output_file = os.path.join(output_folder, f"{video_id}_comments.json")
    
    # Check if we already have the comments for this video
    if os.path.exists(output_file):
        print(f"Comments for {video_id} already exist. Loading from file.")
        with open(output_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Command to download comments
    cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video_id}",
        "--skip-download",  # Don't download the video
        "--write-comments",  # Download comments
        "--output", f"{output_folder}/{video_id}_comments.%(ext)s"
    ]
    
    try:
        print(f"Downloading comments for video {video_id}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error downloading comments for {video_id}: {result.stderr}")
            return []
        
        # yt-dlp saves comments in a JSON file
        comments_file = os.path.join(output_folder, f"{video_id}_comments.info.json")
        
        if not os.path.exists(comments_file):
            print(f"Comments file not found for {video_id}")
            return []
        
        with open(comments_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract comments from the JSON
        comments = []
        for comment in data.get('comments') or []:
            comments.append({
                'text': comment.get('text', ''),
            })

        # Save processed comments to a separate file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
            
        return comments
    
    except Exception as e:
        print(f"Error processing video {video_id}: {str(e)}")
        return []

def get_comments_from_multiple_videos(video_ids, output_folder="comments"):
    """
    Download comments from multiple YouTube videos
    
    Args:
        video_ids (list): List of YouTube video IDs
        output_folder (str): Folder to save the comments
    
    Returns:
        pandas.DataFrame: DataFrame containing all comments
    """
    all_comments = []
    
    for video_id in tqdm(video_ids, desc="Processing videos"):
        comments = get_comments_with_ytdlp(video_id, output_folder)
        all_comments.extend(comments)
        
        # Add a delay between videos to be nice to YouTube
        time.sleep(1)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_comments)
    return df

def save_comments_to_csv(df, output_file="youtube_comments.csv"):
    """Save comments to a CSV file."""
    if df.empty:
        print("No comments to save.")
        return
        
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Saved {len(df)} comments to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Download YouTube comments using yt-dlp")
    parser.add_argument("--videos", nargs="+", help="List of YouTube video IDs")
    parser.add_argument(
        "--output",
        default="/Users/muzaffercikay/Desktop/personel/kurdish-kurmanji-typo-correction/kurdish_comments.csv",
        help="Output CSV file",
    )
    parser.add_argument("--folder", default="comments", help="Folder to save comment files")

    args = parser.parse_args()

    if not args.videos:
        # Example: Get video IDs for Mem Ararat's songs
        video_ids = [
            "xYhC8n8lmxQ",  # Replace with actual Mem Ararat video IDs
            "CRFRZJmf_BM", 
            # Add more video IDs here
        ]
        print("No video IDs provided. Using example video IDs.")
    else:
        video_ids = args.videos

    # Get comments
    comments_df = get_comments_from_multiple_videos(video_ids, args.folder)

    # Save to CSV
    save_comments_to_csv(comments_df, args.output)

    # Print some statistics
    if not comments_df.empty:
        print(f"Total comments collected: {len(comments_df)}")

        # Print language statistics if you have language detection
        # You can add langdetect or other libraries to identify Kurdish comments

if __name__ == "__main__":
    main()
