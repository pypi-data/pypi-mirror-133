import os

from setuptools import find_packages, setup

version_contents = {}
version_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "openai/version.py"
)
with open(version_path, "rt") as f:
    exec(f.read(), version_contents)

setup(
    name="openai-slim",
    description="Python client library for the OpenAI API",
    version=version_contents["VERSION"],
    install_requires=[
        "requests>=2.20",  # to get the patch for CVE-2018-18074
    ],
    extras_require={"dev": ["black~=21.6b0", "pytest==6.*"]},
    python_requires=">=3.7.1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "openai": [
            "data/ca-certificates.crt",
            "py.typed",
        ]
    },
    author="OpenAI",
    author_email="mitranopeter@gmail.com",
    url="https://github.com/PeterMitrano/openai-python-slim",
)
