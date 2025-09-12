import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]


def resolve_resource_path(relative: str) -> str:
    """
    Resolve a resource path relative to the project root in a robust way,
    even when Streamlit changes working directories.
    """
    return str(PROJECT_ROOT.joinpath(relative))
