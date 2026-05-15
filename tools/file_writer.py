import os
from langchain_core.tools import tool


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
