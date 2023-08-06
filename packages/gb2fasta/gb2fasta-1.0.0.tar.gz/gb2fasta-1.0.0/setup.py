from setuptools import setup, find_packages
exec(open('gb2fasta/__init__.py').read())

DESCRIPTION = 'Python CLI to convert .gb file to .fasta.'
LONG_DESCRIPTION = 'Python CLI that converts genbank file format to fasta file format.'

# Setting up
setup(
        name="gb2fasta",
        version= __version__,
        author="James Sanders",
        author_email="james.sanders1711@gmail.com",
        url = 'https://github.com/J-E-J-S/gb2fasta',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'biopython==1.78',
            'click==7.1.2'
        ],
        entry_points = {
            'console_scripts':['gb2fasta=gb2fasta.gb2fasta:cli']
        }
)
