import requests
import os
import random

headers = {'user-agent': 'freaky_script/0.0.1'}

# Get the number of images, ensure it's an integer
num_of_images = input("Num Of Images: ")
try:
    num_of_images = int(num_of_images)
except ValueError:
    print("Please enter a valid integer for the number of images.")
    exit()

# Build the URL
url = f'https://e621.net/posts.json?limit={num_of_images}'
tags = input("Type one tag (separate by space) or just press enter: ").strip()

if tags:
    url += "&tags=" + "+".join(tags.split())

page = input("Which page did you want to search? (Press enter for random): ")
if page:
    url += "&page=" + page
else:
    page = random.randint(1, 15)
    print(f"Using Page {page}!")
    url += "&page=" + str(page)

# Fetch the data
try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()  # Raise an error for bad responses
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# Parse the JSON response
try:
    data = r.json()
except ValueError:
    print("Error parsing JSON response.")
    exit()

# Check if posts are available
if 'posts' in data and len(data['posts']) > 0:
    # Create a directory named 'Images' if it doesn't exist
    os.makedirs('Images', exist_ok=True)

    # Iterate through each post up to the number of images specified
    for i, post in enumerate(data['posts']):
        if i >= num_of_images:  # Ensure not to exceed the requested number of images
            break

        # Get the URL for the image file
        download = post.get('file', {}).get('url')

        if download:
            print(f"Downloading image {i + 1}:", download)

            # Send a GET request to the image URL
            try:
                response = requests.get(download, stream=True)
                response.raise_for_status()  # Raise an error for bad responses
            except requests.RequestException as e:
                print(f"Failed to retrieve image {i + 1}: {e}")
                continue

            # Create a unique file name for each image
            file_name = f"Images/freak_image_{i + 1}.jpg"

            # Open a file in binary write mode to save the image
            with open(file_name, 'wb') as file:
                # Iterate over the response data in chunks to save memory
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image {i + 1} downloaded successfully as {file_name}.")
        else:
            print(f"No valid URL found for image {i + 1}.")
else:
    print("No posts found.")
