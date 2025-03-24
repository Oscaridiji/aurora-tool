# setup.py
from setuptools import setup, find_packages

setup(
    name="aurora-tool",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["boto3", "questionary", "python-dotenv"],
    entry_points={
        "console_scripts": ["aurora-tool=aurora_tool.start:main"],
    },
    author="Oscar Dev",
    author_email="oscaridiji@gmail.com",
    description="CLI Tool para clonar clusters de Aurora para entornos de desarrollo",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)