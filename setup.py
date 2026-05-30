"""CloudScope setup."""

from setuptools import setup, find_packages

setup(
    name="cloudscope",
    version="0.3.1",
    description="Multi-cloud resource monitor and cost optimizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mlresearch-lab",
    author_email="mlresearch.cloudlab@gmail.com",
    url="https://github.com/mlresearch-lab/cloudscope",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "boto3>=1.28",
        "aiohttp>=3.8",
    ],
    extras_require={
        "gcp": ["google-cloud-monitoring>=2.16"],
        "azure": ["azure-mgmt-monitor>=6.0"],
        "all": [
            "google-cloud-monitoring>=2.16",
            "azure-mgmt-monitor>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cloudscope=cloudscope.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
)
