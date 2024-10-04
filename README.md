# Project Setup

This guide will help you set up a virtual environment and install the required dependencies for this project.

## Prerequisites

Ensure you have the following installed on your system:
- **Python 3.6+**: You can check if Python is installed by running `python --version` or `python3 --version` in your terminal.
- **pip**: Python's package installer. Verify installation by running `pip --version`.

## Setting up the Virtual Environment

1. **Create a Virtual Environment**

   Open your terminal and navigate to the project directory, then run the following command to create a virtual environment:

   ```bash
   python3 -m venv venv
    ```


2. **Activate the Virtual Environment**
- On macOS/Linux:
    ```bash
    . .venv/bin/activate
    ```

- On windows:
    ```bash
    .venv\Scripts\activate
    ```
3. **Install the Required Dependencies**

    With the virtual environment activated, run the following command to install all dependencies listed in requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```
