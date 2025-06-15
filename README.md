## ✍️ Related Article

I wrote a short Medium post here:

[🧹 Cleaning Up Notion Export Filenames)](https://medium.com/@jonowschan/cleaning-up-notion-export-filenames-fbf3ebee4005)


If you’ve ever exported a Notion page, you’ve probably seen this:

  ```My Page 8c14a3b7b53f4b908b0f8db1eaa2fb87```


That last part? It’s a unique identifier that Notion adds to keep everything internally linked. It’s technically useful, but when you’re exporting stuff for actual use, it becomes a pain. Two main problems:

- **It looks messy.**
- **The file paths get too long**, especially when nested pages are involved and then you can’t even open them properly on some systems.

![A frustrated emoji looking at a Notion export error](images/Site%20cant%20be%20reached.png)

## 🛠️ The Fix

This Python script renames all the exported files and folders to remove that random string, leaving just the clean title. **It also updates the links _inside_ the `.html` files** so everything still works — no broken internal links when you click around.

## 🧪 How to Use It

1. **Export your Notion pages** as **.HTML** (you’ll find this under `Export > HTML`).
2. **Unzip the export** using [7-Zip](https://www.7-zip.org/) or your tool of choice.
3. **Install the required Python packages** (just once):

    ```bash
    pip install tqdm beautifulsoup4
    ```

4. **Update the `root_dir` path** in the script to point to the folder where you unzipped the export.
5. **Run the script** and enjoy the clean paths.

