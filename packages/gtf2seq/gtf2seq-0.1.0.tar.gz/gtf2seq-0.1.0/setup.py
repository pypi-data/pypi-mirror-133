import ez_setup
import sys
ez_setup.use_setuptools()
from setuptools import setup

# from mpld3
def get_version(path):
    """Get the version info from the mpld3 package without importing it"""
    import ast

    with open(path) as init_file:
        module = ast.parse(init_file.read())

    version = (ast.literal_eval(node.value) for node in ast.walk(module)
               if isinstance(node, ast.Assign)
               and node.targets[0].id == "__version__")
    try:
        return next(version)
    except StopIteration:
        raise ValueError("version could not be located")

install_requires = ["python-docx==0.8.10", 
                    "PyVCF==0.6.8",
                    "pyfaidx"]
if sys.version_info[:2] < (2, 7):
    install_requires.extend(["argparse", "ordereddict"])

setup(name='gtf2seq',
      version=get_version("gtf2seq.py"),
      description="Extract genomic sequences and visualize the genomic features in word document",
      py_modules=['gtf2seq'],
      author="Bix",
      author_email="bix0032@gmail.com",
      license="MIT",
      #url="",
      install_requires=install_requires,
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      classifiers=[
      'Topic :: Scientific/Engineering :: Bio-Informatics', 
      #'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3'
      ],
      scripts=['gtf2seq.py']
)
