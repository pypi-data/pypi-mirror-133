from setuptools import setup, find_packages

MODULE_NAME: str = "dekespo_ai_sdk"

with open("README.md", "r") as f:
    long_description = f.read()

main_ns = dict()
with open("version.py") as f:
    exec(f.read(), main_ns)

setup(
    name=MODULE_NAME,
    packages=find_packages(include=(f"{MODULE_NAME}*",)),
    version=main_ns['__version__'],
    license="apache-2.0",
    description="Dekespo AI SDK tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Deniz Kennedy",
    author_email="denizkennedy@gmail.com",
    url="https://github.com/dekespo/dekespo_ai_sdk_py",
    keywords=["SDK", "AI", "Tool"],
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)