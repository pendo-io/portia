import ingest_data_neo4j
import subprocess
from sys import platform
import click
import time

class PlatformNotSupported(Exception):
    '''
    Raised if attempted to be run on a non-supported platform.
    '''
    pass

@click.command()
@click.argument('filepath', required=True)
def run_dependency_check_tool(filepath):
    '''
    Checks the platform of the system running the program to ensure that the
    proper executable version of DependencyCheck. If the platform is not
    supported, raise an exception.

    Input: The filepath of the dependency file.

    Output: Prints out DependencyCheck as it is running.
    '''   
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
            print(line.decode('utf-8', errors='ignore').strip())
        process.stdout.close()
        print(process.wait())
        time.sleep(5)
        # print(process.stdout.read())
    else:
        raise PlatformNotSupported("Please run this on a Linux, Mac, or Windows machine")
    print("-------------------------------------------")
if __name__ == "__main__":
    #"C:\\Users\\minew\\Downloads\\nancy-main\\nancy-main"
    run_dependency_check_tool()
    print("CHECK for Json file")
    print("Run Pendo Processes with json file")
    print("DELETE Json file")
    print("FORCE open neo4J")
    print("All while it print logs to user so they know shtuff happening")