from setuptools import setup, find_packages

setup(
    name="todo-cli",
    version="1.0.0",
    description="A simple yet complete command-line To-Do List app.",
    author="Your Name",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "todo=todo.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
