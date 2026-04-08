from setuptools import setup, find_packages
import subprocess
import os


# 🔧 Auto-install pre-commit hook
def install_git_hook():
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"],
                                stderr=subprocess.DEVNULL)
        print("[sentinel] Installing pre-commit hook...")
        subprocess.run(["pre-commit", "install"], check=True)
        print("[sentinel] Pre-commit hook installed successfully!")
    except Exception:
        print("[sentinel] Not a git repository. Skipping hook installation.")


# 🚀 Setup config
setup(
    name="sentineldetectai",
    version="0.2.0",  # 🔥 upgraded version
    author="A. Veda Sree",
    author_email="avedasree2885@gmail.com",
    description="AI-powered pre-commit security scanner and memory leak detector for Python",
    
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",

    url="https://github.com/vedasree28/SentinelCodeAI",

    packages=find_packages(),
    python_requires=">=3.10",

    install_requires=[
        "rich",
        "pre-commit",   # ✅ REQUIRED for hook
        "pylint",
        # transformers optional (heavy) → keep only if needed
    ],

    entry_points={
        "console_scripts": [
            "sentinel=src.cli.main:main",
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


# 🔥 Run hook install AFTER setup
if __name__ == "__main__":
    install_git_hook()