import nox

# Define the default sessions to run
nox.options.sessions = ["tests"]


# Define the test session with multiple Python versions
@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def tests(session):
    """
    Test session to synchronize and run tests across multiple Python versions.
    """
    # Pass through the PYTHON_VERSION environment variable if set
    # Otherwise, set it to the current session's Python version
    if "PYTHON_VERSION" not in session.env:
        session.env["PYTHON_VERSION"] = session.python

    # Allow external commands by specifying 'external=True'
    # Run 'uv sync --python {envpython}'
    session.run("uv", "sync", "--python", session.python, external=True)

    # Run 'uv run python -m pytest --doctest-modules tests --cov --cov-config=pyproject.toml --cov-report=xml'
    session.run(
        "uv",
        "run",
        "python",
        "-m",
        "pytest",
        "--doctest-modules",
        "tests",
        external=True,
    )

    # Run 'mypy' for type checking
    session.run("mypy", external=True)
