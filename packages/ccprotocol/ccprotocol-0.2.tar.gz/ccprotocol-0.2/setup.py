from distutils.core import setup
setup(
    name="ccprotocol",
    packages=["ccprotocol"],
    version="0.2",
    license="MIT",
    description="A python implementation of the CC Protocol.",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/py-ccprotocol",
    download_url="https://github.com/bossauh/py-ccprotocol/archive/refs/tags/v_02.tar.gz",
    keywords=["utility", "api", "minecraft", "computer craft", "protocol"],
    install_requires=[
        "fluxhelper"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
