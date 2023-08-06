import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplelayoutzzh",
    version="0.0.1",
    author="piglet94",
    author_email="715654107@qq.com",
    description="A small study package",
    package_dir={"": "src"},
    packages=setuptools.find_packages(include=['src', 'src.*']),
    python_requires=">=3.0",
    install_requires=['numpy','argparse','matplotlib','scipy'],
    entry_points={'console_scripts': ['simplelayout=simplelayout.__main__:main']}
)