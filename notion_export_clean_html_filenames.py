import os
import re
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup

# ---------------------------------------------
# 🧠 Setup
# ---------------------------------------------

# Regex pattern to match Notion's 32-character hash suffix (e.g. "My Page 9b30b13b97a74acda7dd1f152937e173.html")
HASH_PATTERN = re.compile(r' ([0-9a-f]{32})(\.[^.]+)?$')

# Removes the hash (and keeps file extension if present)
def remove_hash_suffix(name):
    return HASH_PATTERN.sub(lambda m: m.group(2) or '', name)

# Recursively walk through all files and folders from bottom-up
# This order avoids renaming a folder before its contents are handled
def get_all_paths(root_dir):
    """Get all files and folders in bottom-up order."""
    paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for fname in filenames:
            paths.append(('file', dirpath, fname))
        for dname in dirnames:
            paths.append(('dir', dirpath, dname))
    return paths

# ---------------------------------------------
# 📝 Renaming Files and Folders
# ---------------------------------------------

def rename_items(root_dir):
    """
    Rename all files/folders by removing the Notion hash suffix.
    Returns a mapping of original name → cleaned name (just base names, not full paths).
    """
    name_map = {}
    paths = get_all_paths(root_dir)

    for kind, dirpath, name in tqdm(paths, desc="Renaming files/folders", unit="item"):
        new_name = remove_hash_suffix(name)
        if new_name != name:
            old_path = os.path.join(dirpath, name)
            new_path = os.path.join(dirpath, new_name)
            if not os.path.exists(new_path):  # Avoid accidental overwrite
                os.rename(old_path, new_path)
                name_map[name] = new_name  # Only store name-level mappings (not full paths)
    return name_map

# ---------------------------------------------
# 🔗 Updating Internal HTML Links
# ---------------------------------------------

def update_html_links(root_dir, name_map):
    """
    Go through each .html file and update links (href/src)
    so they point to the newly renamed files/folders.
    """
    html_files = []

    # Find all .html files in the export
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".html"):
                html_files.append(os.path.join(dirpath, fname))

    for html_path in tqdm(html_files, desc="Fixing internal links", unit="file"):
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        changed = False

        # Check all <a> and <img> tags for broken or outdated internal links
        for tag in soup.find_all(['a', 'img']):
            attr = 'href' if tag.name == 'a' else 'src'
            if tag.has_attr(attr):
                original_url = tag[attr]
                decoded = urllib.parse.unquote(original_url)  # Convert %20 etc. to normal chars
                parts = decoded.split('/')

                # Replace each segment if it was renamed
                new_parts = [name_map.get(p, p) for p in parts]
                new_path = '/'.join(new_parts)

                if new_path != decoded:
                    tag[attr] = urllib.parse.quote(new_path)  # Convert back to URL-safe format
                    changed = True

        # Overwrite the HTML file if anything changed
        if changed:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(str(soup))

# ---------------------------------------------
# 🚀 Run it
# ---------------------------------------------

# 🔧 Set this to the folder where your Notion export was unzipped
root_dir = r'C:\Path\To\Notion\Export.html'

print(f"📁 Starting cleanup of: {root_dir}")
name_map = rename_items(root_dir)

print(f"🔗 Updating HTML internal links...")
update_html_links(root_dir, name_map)

print("✅ Done! Filenames cleaned and internal links updated.")
