# Cloudy4Win - Cloud File Management Application

Cloudy4Win is a Windows desktop application built with the Flet framework and Cloudflare R2 for cloud storage. It allows users to upload, download, share, preview, rename, and manage their files in the cloud, all within a user-friendly interface.

## Features

*   **Pin-Protected Access:** Secure access to the application using a 6-digit PIN (default: `202526`).
*   **File Upload:** Upload single or multiple files to the cloud.
*   **File Listing:** View a list of uploaded files, including their name, size, and type.
*   **File Preview:** Preview images and videos directly within the app (using presigned URLs).
*   **File Download:** Download files from the cloud to your local machine.
*   **File Deletion:** Delete files from the cloud.
*   **File Sharing:** Generate presigned URLs to share files with others.
*   **File Rename:** Rename files directly from the UI.
*   **Bulk Actions:** Select multiple files for bulk deletion or downloading.
*   **Sorting:** Sort files by name, size, or date.
*   **Filtering:** Filter files by name.
*   **Drag & Drop:** Upload files by dragging and dropping them onto the app window.
*   **Upload Progress:** See upload progress with a visual progress bar.
*   **Settings:** Check the application version and check for updates (redirects to a website).
*   **Cloudflare R2 Integration:** Uses Cloudflare R2 for cloud storage.
*   **Responsive design:** Application responsive and use default flet theme.

## Technologies Used

*   **Flet:** A Python framework for building real-time web, mobile, and desktop apps.
*   **Cloudflare R2:** Object storage for storing files.
*   **Boto3:** The AWS SDK for Python, used to interact with Cloudflare R2 (S3-compatible API).
*   **Python:** The primary programming language.
* **Pyperclip**: A cross-platform Python module for copy and paste clipboard functions.

## Prerequisites

*   **Python 3.11+** installed on your Windows machine.
*   **Pip** (Python package installer) installed.

## Installation

1.  **Clone the repository (or download the source code):**

    ```bash
    git clone <repository-url>
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd cloudy4win
    ```

3.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```
    Or install library manually.
    ```bash
    pip install flet boto3 pyperclip
    ```

## Configuration

1.  **Cloudflare R2 Credentials:**
    *   Open the `src/r2.py` file.
    *   Update the following variables with your Cloudflare R2 credentials:

        ```python
        self.endpoint = 'https://<your-r2-endpoint>.r2.cloudflarestorage.com'
        self.access_key_id = '<your-access-key-id>'
        self.secret_access_key = '<your-secret-access-key>'
        self.bucket_name = '<your-bucket-name>'
        self.prefix = '<your-prefix>/' # Example : cloudy4win/
        ```

## How to Run

1.  **Navigate to the project directory** in your command prompt or terminal.
2.  **Run the application:**

    ```bash
    python src/main.py
    ```

3.  **Pin Verification:** The application will prompt you to enter the 6-digit PIN. Enter `202526` to proceed.

## Usage

*   **Upload Files:** Click the "Upload File" button or drag and drop files onto the application window.
*   **Manage Files:** Use the file list to perform actions:
    *   **Delete:** Delete a file.
    *   **Rename:** Rename a file.
    *   **Share:** Copy a presigned URL to share the file.
    *   **Download:** Download a file to your local machine.
    *   **Preview:** Preview images and videos.
    *   **Bulk Actions:** Select multiple files with the checkboxes and use the "Delete Selected" or "Download Selected" buttons.
* **Sorting and Filtering** :
    * use the sorting dropdown to sort the files.
    * use the filter textfield to filter the files.
*   **Settings:** Click the settings icon (gear) in the app bar to view the version and check for updates.

## Troubleshooting

*   **`AttributeError: module 'flet' has no attribute 'FileDropEvent'`:**
    *   This error means that you are using an older version of Flet.
    *   Uninstall flet `pip uninstall flet-cli flet-desktop flet-web flet`
    *   install flet `pip install flet`
    *   Delete the `__pycache__` directories and `.pyc` files.
    *  Run your app using `python src/main.py`
*  **Error with Boto3 or R2**:
    * Make sure your credential are correct.
    * check the permissions of your bucket.

## Future Improvements

*   **Preview More File Types:** Add support for PDFs, text files, and other common formats.
* **Caching for Faster Access:** Implement caching to further improve performance.
*   **Enhanced Security:** Implement more robust authentication and authorization.
*   **User Management:** Add support for multiple users.

## License

This project is open-source.

---

This `README.md` provides a good overview of your project and should help other developers understand, set up, and use Cloudy4Win. Remember to replace placeholders like `<repository-url>`, `<your-r2-endpoint>`, etc., with your actual information.
