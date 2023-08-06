import os
import sys
import click
from Bio import SeqIO

def _getVersion(ctx,param, value):

    if not value or ctx.resilient_parsing:
        return
    folder = os.path.abspath(os.path.dirname(__file__))
    init = os.path.join(folder, '__init__.py')
    f = open(init, 'r')
    version = f.read()
    version = version.replace('__version__ = ', '')
    version = version.replace('\'', '')
    version = version.replace('\n', '' )
    f.close()
    click.echo(version)
    ctx.exit()

@click.command()
@click.argument('file')
@click.option('-v', '--version', is_flag=True, callback=_getVersion, expose_value=False, is_eager=False, help='Show version number and exit.')
def cli(file):

    """Arguments:\n
    File GenBank file (.gb) to convert to fasta format (.fasta).

    """
    # check input file is.gb
    if file.endswith('.gb') != True:
        click.echo('Invalid file format.')
        click.echo('Genbank file format only (.gb)')
        return

    # Check file exists
    if os.path.isfile(file) != True:
        click.echo('File does not exist.')
        return

    # extracts original genbank file name
    outFile = os.path.basename(os.path.splitext(file)[0])

    # check file doesn't already exist
    count = 1
    while os.path.isfile(outFile + '.fasta'):
        if count == 1:
            outFile = outFile + ' ({count})'.format(count=count)
        else:
            outFile = ' '.join(outFile.split()[0:-1]) + ' ({count})'.format(count=count)
        count += 1

    # convert .gb to .fasta
    # checks for errors in gb file
    try:
        SeqIO.convert(file, 'genbank', outFile + '.fasta', 'fasta')
    except ValueError:
        click.echo('An error has occurred, check .gb fidelity.')
        os.remove(outFile + '.fasta')
        return

if __name__ == '__main__':
    cli()
