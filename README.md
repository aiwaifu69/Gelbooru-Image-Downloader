Gelbooru Image Downloader
This Python script allows you to download images from Gelbooru based on tags. The script reads tags from a text file, downloads images associated with each tag, and saves them in separate folders. The script also handles delays between requests to avoid overloading the server.

Repository Name
Gelbooru-Image-Downloader

Description
A Python script to download images from Gelbooru based on tags. The script handles delays between requests, downloads images in parallel, and saves images in separate folders for each tag.

Installation
Clone this repository to your local machine using git clone https://github.com/yourusername/Gelbooru-Image-Downloader.git.

Navigate to the cloned repository using cd Gelbooru-Image-Downloader.

Install the required Python packages using pip:

bash
Copy code
pip install requests
Usage
Create a text file named tags.txt in the same directory as the script. Each line of the file should contain one tag.

Run the script using Python:

bash
Copy code
python main.py
A GUI will open asking for the tags.txt file and the output folder. Select the tags.txt file and the folder where you want to save the images.

The script will start downloading images for each tag. The images will be saved in separate folders for each tag in the output folder.

After a tag is processed, the script will add a prefix 'done_' and a suffix '_image_count' to the tag in the tags.txt file.

If the script encounters an error while processing a tag, it will add the tag to an ignore.txt file in the output folder.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Please replace yourusername with your actual GitHub username in the git clone command. Also, you might want to add a LICENSE.md file to your repository if you want to include a license for your project.
