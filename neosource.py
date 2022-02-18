import ingest_data_neo4j
import subprocess
from sys import platform, exit
import os
import json
import argparse
from time import sleep

class PlatformNotSupported(Exception):
    '''
    Raised if attempted to be run on a non-supported platform.
    '''
    pass

def remove_json(dir_path):
    sleep(10)
    os.remove(dir_path + 'dependency-check-report.json')

def check_json(dir_path):
    '''
    Verifies that the JSON file is valid. This means the JSON file that DependencyCheck output has dependencies listed. If no dependencies listed, the file will be considered invalid.
    '''
    print("Validating JSON file",flush=True)
    with open(dir_path + 'dependency-check-report.json') as file:
        output = json.load(file)
        if not output['dependencies']:
            print('\nError: Dependency Check found 0 dependencies in the provided file/path. The filepath specified may not be a valid dependency file.\n(If you are attempting to scan a go.mod file, make sure you have Golang installed.)\n')
            file.close()
            os.remove('dependency-check-report.json')
            # Make sure to delete json file before exiting probably.
            exit(1)

def run_dependency_check_tool(filepath, dir_path):
    '''
    Checks the platform of the system running the program to ensure that the
    proper executable version of DependencyCheck. If the platform is not
    supported, raise an exception. If the filepath doesn't exist or no
    dependency file is found, exit.

    Input: The filepath of the dependency file. The dirpath is wherever neosource executable is.

    Output: Prints out DependencyCheck as it is running.
    '''

    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
        print("\nError: Not a valid filepath. \n\nTry 'neosource.py -h' for help.")
        exit(1)

    print("Starting dependency-check:")
    print("-------------------------------------------")
    

    if platform == 'linux' or platform == 'linux2' or platform == 'darwin': ## If the Computer is a Mac or Linux
        dir_path = dir_path + '/'
        if not os.path.isfile("dependency-check/bin/dependency-check.sh"):
            print("Dependency Check cannot be found.")
            exit(1)
        process = subprocess.Popen([dir_path + 'dependency-check/bin/dependency-check.sh', '-s', filepath,'-o', dir_path + '/dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip())
        process.stdout.close()
        process.wait()
    elif platform == 'win32' or platform == 'cygwin': ## If the Computer is a Windows
        dir_path = dir_path + '\\'
        process = subprocess.Popen([dir_path + 'dependency-check\\bin\\dependency-check.bat', '-s', filepath,'-o', dir_path +'\\dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip(), flush = True)
        process.stdout.close()
        process.wait()
    else:
        raise PlatformNotSupported("Please run this on a Linux, Mac, or Windows machine")
    print("-------------------------------------------")
    return dir_path


if __name__ == "__main__":
    #"C:\\Users\\minew\\Downloads\\nancy-main\\nancy-main"
    parser = argparse.ArgumentParser(description='A tool that runs DependencyCheck on the given file path, then puts it into Neo4J.')
    parser.add_argument('filepath', help='the file path to run dependency check on')
    # parser.add_argument('project', help='The name of the project being scanned')
    
    args = parser.parse_args()
    filepath = args.filepath
    print(filepath)
    # project = args.project
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = run_dependency_check_tool(filepath, dir_path)
    check_json(dir_path)
    remove_json(dir_path)
    print("Run Pendo Processes with json file")
    print("DELETE Json file")
    print("FORCE open neo4J")
    print("All while it print logs to user so they know shtuff happening")