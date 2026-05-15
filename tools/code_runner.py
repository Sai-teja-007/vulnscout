import subprocess
import tempfile
import os
from langchain_core.tools import tool

@tool
def code_runner(code: str) -> str:
    """
    Write and execute Python code. Use this when you need to:
    - run calculations
    - process data
    - test a fix or patch
    - verify logic
    Input: valid Python code as a string.
    Returns the output (stdout) or error message.
    """
    # Write code to a temp file and run it in a subprocess
    # This keeps it isolated from the main process
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_path = f.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=15,        # kills the process if it runs more than 15s
        )

        os.unlink(temp_path)   # clean up temp file

        output = ""
        if result.stdout:
            output += f"Output:\n{result.stdout}"
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"

        return output.strip() if output.strip() else "Code ran successfully with no output."

    except subprocess.TimeoutExpired:
        return "Code timed out after 15 seconds. Simplify the code."
    except Exception as e:
        return f"Failed to run code: {str(e)}"