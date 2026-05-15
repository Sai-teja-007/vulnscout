import os
from langchain_core.tools import tool

@tool
def file_reader(filepath: str) -> str:
    """
    Read the contents of a file.
    Use this when the user uploads a file and you need to analyze it.
    Input: file path relative to the project folder (e.g. 'uploads/report.txt').
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, filepath)

        if not os.path.exists(full_path):
            return f"File not found: {filepath}. Make sure it's inside the 'uploads' folder."

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 4000:
            return content[:4000] + "\n\n[...trimmed to first 4000 characters]"

        return content

    except Exception as e:
        return f"Could not read file: {str(e)}"


@tool
def file_writer(input: str) -> str:
    """
    Save text content to a file in the reports folder.
    Use this to save final answers, summaries, or reports.
    Input format: 'filename.txt|||content to save'
    """
    try:
        if "|||" not in input:
            return "Wrong format. Use: 'filename.txt|||content to save'"

        filename, content = input.split("|||", 1)
        filename = filename.strip()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(base_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)

        full_path = os.path.join(reports_dir, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File saved successfully: reports/{filename}"

    except Exception as e:
        return f"Could not save file: {str(e)}"