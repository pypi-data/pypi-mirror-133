from setuptools import setup, find_packages
# from setuptools.command.install import install as _install
#
#
# class Install(_install):
#     def run(self):
#         _install.do_egg_install(self)
#         import nltk
#         nltk.download('stopwords')
#         nltk.download('punkt')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    # cmdclass={'install': Install},
    name="text-based-clusterer",
    version="0.0.2",
    author="Benedict Taguinod",
    author_email="benedict.a.taguinod@gmail.com",
    description="A package that clusters python objects based on a chosen string attribute",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/btaguinod/text-based-clusterer",
    project_urls={
        "Bug Tracker": "https://github.com/btaguinod/text-based-clusterer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['numpy', 'nltk'],
)
