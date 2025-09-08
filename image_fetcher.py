#!/usr/bin/env python3

import requests
import os
from urllib.parse import urlparse

def fetch_image(url):
    """Function to fetch and save a single image from a URL."""
    try:
        # Make request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check if the response is actually an image
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f" Skipping: {url} (Not an image, Content-Type={content_type})")
            return

        # Extract filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename, assign a default one
        if not filename:
            filename = "downloaded_image.jpg"

        # Build the full path
        filepath = os.path.join("Fetched_Images", filename)

        # Check for duplicates
        if os.path.exists(filepath):
            print(f" Skipped duplicate: {filename}")
            return

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f" Successfully fetched: {filename}")
        print(f"   Saved to: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f" Connection error for {url}: {e}")
    except Exception as e:
        print(f" An error occurred: {e}")


def main():
    print(" Welcome to the Ubuntu Image Fetcher (Extended)")
    print("A tool for respectfully collecting and organizing images\n")

    # Create directory if it doesn’t exist
    os.makedirs("Fetched_Images", exist_ok=True)

    # Ask user for multiple URLs (comma separated)
    urls = input(" Enter one or more image URLs (separated by commas): ")

    # Split input into a list of URLs
    url_list = [u.strip() for u in urls.split(",") if u.strip()]

    # Process each URL
    for url in url_list:
        fetch_image(url)

    print("\n All done! Community enriched, images organized.")


if __name__ == "__main__":
    main()
