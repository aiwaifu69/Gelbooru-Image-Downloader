import os
import json
import time
import requests
import threading
from tkinter import filedialog
from tkinter import Tk, messagebox
from urllib.parse import quote

def get_image_links(tag, delay):
    # Encode tag for URL
    tag = quote(tag)
    links = []
    pid = 0

    # Define allowed image extensions
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.webp']

    while True:
        url = f'https://gelbooru.com/index.php?page=dapi&json=1&s=post&q=index&limit=100&tags={tag}&pid={pid}'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        # If 'post' key does not exist in the response, break the loop
        if 'post' not in data:
            break

        # If no more images, break the loop
        if not data['post']:
            break

        # Add image links to the list if the file extension is allowed
        for post in data['post']:
            if os.path.splitext(post['file_url'])[1] in allowed_extensions:
                links.append(post['file_url'])

        pid += 1

        # Delay between requests
        time.sleep(delay)
        # Increase delay
        delay += 0.01

    return links, delay

def download_image(link, tag_folder):
    filename = os.path.join(tag_folder, link.split('/')[-1])

    # Check if image already exists
    if os.path.exists(filename):
        print(f'Image {filename} already exists, skipping download')
        return

    response = requests.get(link)

    # Save the image
    with open(filename, 'wb') as file:
        file.write(response.content)

def download_images(links, tag, output_folder, delay):
    tag_folder = os.path.join(output_folder, tag)

    # Create tag directory if it doesn't exist
    if not os.path.exists(tag_folder):
        os.makedirs(tag_folder)

    for i in range(0, len(links), 10):  # Change this line
        threads = []

        # Start new threads for each image download
        for link in links[i:i+10]:  # And this line
            thread = threading.Thread(target=download_image, args=(link, tag_folder))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Print progress
        print(f'Tag_name={tag}, Downloading={i+10}/{len(links)}, Total percentage={((i+10)/len(links))*100:.2f}%')  # And this line

        # Delay between requests
        time.sleep(delay)
        # Increase delay
        delay += 0.01

    return delay

def main():
    # Create a GUI for folder selection
    root = Tk()
    root.withdraw()

    # Ask for the tags.txt file and output folder
    tags_file = filedialog.askopenfilename(title='Select tags.txt File')
    output_folder = filedialog.askdirectory(title='Select Output Folder')

    ignored_tags = []

    # Read the tags.txt file
    with open(tags_file, 'r') as file:
        tags = [line.strip() for line in file]

    # Create a dictionary to store the tag and its image count
    tag_image_count = {}

    # Download images for each tag
    for tag in tags:
        # Skip processed tags
        if tag.startswith('done_'):
            continue

        # Initial delay
        delay = 1
        try:
            links, delay = get_image_links(tag, delay)
            if links:
                tag_image_count[tag] = len(links)
                delay = download_images(links, tag, output_folder, delay)
                # Mark processed tag with prefix 'done_' and suffix '_image_count'
                index = tags.index(tag)
                tags[index] = 'done_' + tag + '_' + str(tag_image_count[tag])
                # Write updated tags back to file immediately after a tag is processed
                with open(tags_file, 'w') as file:
                    for tag in tags:
                        file.write(tag + '\n')
            else:
                print(f'No images found for tag {tag}')
                ignored_tags.append(tag)
        except Exception as e:
            print(f'Error downloading images for tag {tag}: {e}')
            ignored_tags.append(tag)
            continue

    # Write ignored tags to file
    with open(os.path.join(output_folder, 'ignore.txt'), 'w') as file:
        for tag in ignored_tags:
            file.write(tag + '\n')

    messagebox.showinfo("Completed", "Image download completed")

if __name__ == '__main__':
    main()