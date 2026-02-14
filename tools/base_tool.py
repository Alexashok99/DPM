# tools/base_tool.py

class BaseTool:
    """Base class for all tools.
    Attributes:
    name (str): Tool name for display.
    description (str): Tool description for display.
"""

    name: str = "Unnamed Tool"
    description: str = "No description"

    def run(self) -> None:
        """Execute the tool's main functionality.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError
