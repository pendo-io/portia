from argparse import ArgumentParser
from json import load
from os import path, remove
from subprocess import Popen, PIPE
from sys import platform, exit, stderr
from webbrowser import open as open_browser

import ingest_data_neo4j


class PlatformNotSupported(Exception):
    '''
    Raised if attempted to be run on a non-supported platform.
    '''
    pass

def remove_json(dir_path):
    '''
    Remove the JSON file that DependencyCheck generates to aid in cleanup.
    '''
    print("[INFO] Removing json file",flush=True)
    try:
        remove(dir_path + 'dependency-check-report.json') #add continue running after failed remove
    except:
        pass

def check_json(dir_path):
    '''
    Verifies that the JSON file is valid. This means the JSON file that DependencyCheck output has dependencies listed. If no dependencies listed, the file will be considered invalid.
    '''
    print("[INFO] Validating JSON file",flush=True)
    with open(dir_path + 'dependency-check-report.json') as file:
        output = load(file)
        try:
            if output['scanInfo']['analysisExceptions']:
                print("[ERROR] If you are attempting to scan a go.mod file, make sure you have Golang installed.\n", file=stderr)
                remove_json(dir_path)
                exit(0)
        except KeyError:
            print("[INFO] JSON file successfully validated",flush=True)
        if not output['dependencies']:
            print('\n[ERROR] Dependency Check found 0 dependencies in the provided file/path. The filepath specified may not be a valid dependency file.', file=stderr)
            remove_json(dir_path)
            exit(0)

def run_dependency_check_tool(filepath, dir_path):
    '''
    Checks the platform of the system running the program to ensure that the
    proper executable version of DependencyCheck. If the platform is not
    supported, raise an exception. If the filepath doesn't exist or no
    dependency file is found, exit.

    Input: The filepath of the dependency file. The dirpath is wherever neosource executable is.

    Output: Prints out DependencyCheck as it is running.
    '''

    if not path.isfile(filepath) and not path.isdir(filepath):
        print("\n[ERROR] Not a valid filepath. \n\nTry 'neosource.py -h' for help.", file=stderr)
        exit(0)

    print("[INFO] Starting dependency-check:")
    print("-------------------------------------------",flush=True)
    

    if platform == 'linux' or platform == 'linux2' or platform == 'darwin': ## If the Computer is a Mac or Linux
        dir_path = dir_path + '/'
        if not path.isfile(dir_path + "dependency-check/bin/dependency-check.sh"):
            print("[ERROR] Dependency Check cannot be found.", file=stderr)
            exit(0)
        process = Popen([dir_path + 'dependency-check/bin/dependency-check.sh', '-s', filepath,'-o', dir_path + '/dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip())
        process.stdout.close()
        process.wait()
    elif platform == 'win32' or platform == 'cygwin': ## If the Computer is a Windows
        dir_path = dir_path + '\\'
        if not path.isfile(dir_path + "dependency-check\\bin\\dependency-check.bat"):
            print("[ERROR] Dependency Check cannot be found.", file=stderr)
            exit(0)
        process = Popen([dir_path + 'dependency-check\\bin\\dependency-check.bat', '-s', filepath,'-o', dir_path +'\\dependency-check-report.json', '-f', 'JSON', '--enableExperimental'], stdout=PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8', errors='ignore').strip(), flush = True)
        process.stdout.close()
        process.wait()
    else:
        raise PlatformNotSupported("[ERROR] Please run this on a Linux, Mac, or Windows machine", file=stderr)
    print("-------------------------------------------",flush=True)
    return dir_path

def pendoProccess(project, dir_path):
    '''
    Call the Pendo processes responsible for validating that the
    specified Neo4J instance is accessible, making
    dependency-check-report.json Neo4J friendly, and putting the
    dependencies and vulnerabilities in Neo4J.
    '''
    ingest_data_neo4j.run_cli_scan(project, dir_path + 'dependency-check-report.json')

if __name__ == "__main__":
    
    parser = ArgumentParser(description='A tool that runs DependencyCheck on the given file path, then puts it into Neo4J.')
    parser.add_argument('filepath', help='the file path to run dependency check on')
    parser.add_argument('-p','--project', help='This will be the name neo4j will call your project')
    parser.add_argument('-b','--browser', help='This will enable the program to open neo4j in the browser after the code has finished running', action="store_true")

    args = parser.parse_args()
    filepath = args.filepath
    print('[INFO] ' + filepath)
    project = args.project
    if project == None:
        project = 'project'

    ingest_data_neo4j.neo4JCheck()

    dir_path = path.dirname(path.realpath(__file__))
    dir_path = run_dependency_check_tool(filepath, dir_path)
    check_json(dir_path)
    pendoProccess(project, dir_path)
    remove_json(dir_path)
    db2 = ingest_data_neo4j.getDB().split(':')[1][2:] 
    
    if args.browser:
        open_browser('http://'+ db2 +':7474/browser', new=1) ##MAKE THIS OPTIONAL!
    print("[INFO] Open up Neo4J to view results.\nhttp://" + db2 + ":7474/\n[INFO] Run the query 'MATCH (n) RETURN n' to view all results")