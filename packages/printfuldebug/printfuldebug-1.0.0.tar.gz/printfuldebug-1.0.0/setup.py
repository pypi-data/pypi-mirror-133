from setuptools import setup, find_packages

with open("README.md", "w+") as file:
    file.write("If you use print() alot and feel like you want to spice it up a litle then this package is the best choice.")

setup(
    name="printfuldebug",
    version="1.0.0",
    author="yuma061",
    author_email="",
    description="print() but for nerds.",
    long_description_content_type="text/markdown",
    long_description="If you use print() alot and feel like you want to spice it up a litle then this package is the best choice.",
    packages=find_packages(),
    install_requires=["colorama", "psutil"],
    keywords=["python", "print"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)