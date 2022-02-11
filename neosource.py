import ingest_data_neo4j
import subprocess
from sys import platform
import click
import time
import os
import json

class PlatformNotSupported(Exception):
    '''
    Raised if attempted to be run on a non-supported platform.
    '''
    pass

def check_json():
    '''
    Verifies that the JSON file is valid. This means the JSON file that DependencyCheck output has dependencies listed. If no dependencies listed, the file will be considered invalid.
    '''
    print("Validating JSON file",flush=True)
    with open('dependency-check-report.json') as file:
        output = json.load(file)
        if not output['dependencies']:
            print('\nError: Dependency Check found 0 dependencies in the provided file/path. The filepath specified may not be a valid dependency file.\n')
            file.close()
            os.remove('dependency-check-report.json')
            # Make sure to delete json file before exiting probably.
            exit(1)



@click.command()
@click.argument('filepath', required=True)
def run_dependency_check_tool(filepath):
    '''
    filepath: The filepath of a dependency file being scanned
    '''

    '''
    Checks the platform of the system running the program to ensure that the
    proper executable version of DependencyCheck. If the platform is not
    supported, raise an exception. If the filepath doesn't exist or no
    dependency file is found, exit.

    Input: The filepath of the dependency file.

    Output: Prints out DependencyCheck as it is running.
    '''   

    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
        print("\nError: Not a valid filepath. \n\nTry 'neosource.py --help' for help.")
        exit(1)

    print("Starting dependency-check:")
    print("-------------------------------------------")
    if platform == 'linux' or platform == 'linux2' or platform == 'darwin': ## If the Computer is a Mac or Linux
        process = subprocess.Popen(['dependency-check/bin/dependency-check.sh', '-s', filepath,'-o', 'dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip())
        process.stdout.close()
        process.wait()
    elif platform == 'win32' or platform == 'cygwin': ## If the Computer is a Windows
        process = subprocess.Popen(['dependency-check\\bin\\dependency-check.bat', '-s', filepath,'-o', 'dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip(), flush = True)
        process.stdout.close()
        process.wait()
    else:
        raise PlatformNotSupported("Please run this on a Linux, Mac, or Windows machine")
    print("-------------------------------------------")

    check_json() ## Move to main when fixed

if __name__ == "__main__":
    #"C:\\Users\\minew\\Downloads\\nancy-main\\nancy-main"
 
    run_dependency_check_tool()
    print("CHECK for Json file")
    print("Run Pendo Processes with json file")
    print("DELETE Json file")
    print("FORCE open neo4J")
    print("All while it print logs to user so they know shtuff happening")