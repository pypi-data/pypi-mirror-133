import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION") as f:
      v = int(f.read().strip())

setuptools.setup(
    name="pangdoc",
    version=f"0.0.{v}",
    author="Yongfu Liao",
    author_email="liao961120@gmail.com",
    description="Google Docs Workflow for Pandoc Academic Writing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liao961120/pangdoc",
    package_dir = {'': 'src'},
    packages=['pangdoc'],
    install_requires=['pypandoc'],
    package_data={
        "": ["data/*.lua", "data/code.md"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# pypandoc
# filters = ['pandoc-citeproc']
# pdoc_args = ['--mathjax',
#              '--smart']
# output = pypandoc.convert_file(filename,
#                                to='html5',
#                                format='md',
#                                extra_args=pdoc_args,
#                                filters=filters)
