from neo4j import GraphDatabase, exceptions
from os import path
from sys import platform

import get_dc_data

dir_path = path.dirname(path.realpath(__file__))
   
if platform == 'linux' or platform == 'linux2' or platform == 'darwin': ## If the Computer is a Mac or Linux
    dir_path = dir_path + '/'
elif platform == 'win32' or platform == 'cygwin': ## If the Computer is a Windows
    dir_path = dir_path + '\\'

#Read in config.in to authenticate with Neo4J
try:
    l = list()
    with open(dir_path + 'config.in') as file:
        for line in file.readlines():
            parts = line.split('=')
            l.append(parts[1].strip())
    pwd = l.pop()
    user = l.pop()
    db = l.pop()
except Exception:
    print('[ERROR] The config.in file is invalid.')
    exit(1)

#Run these before run_cli_scan can run
driver = GraphDatabase.driver(db, auth=(user, pwd))
tx = driver.session()

def neo4JCheck():
    '''
    Ensure that Neo4J is installed, running, and that hte credentials
    provided in config.in are valid.
    '''
    print("[INFO] Validating neo4j instance",flush=True)
    try:
        tx.run(''' MATCH (n) RETURN n ''')  #Runs a Generic Query to try and connect to the database
        print("[INFO] A valid NEO4J existence!",flush=True)
    except exceptions.ServiceUnavailable:
        print("[ERROR] Invalid neo4j instance\nPlease make sure neo4j is installed and running")
        exit(1)
    except exceptions.AuthError:
        print("[ERROR] Invalid neo4j credentials\nPlease make sure your credentials are correct")
        exit(1)

def getDB():
    '''
    Get the string representation of the IP address
    '''
    return db

def run_cli_scan(project, file):
    '''
    Ingest dependency-check-report.json into a representation that
    Neo4J can use, and then put the data in Neo4J.
    '''
    if not file:
        file = 'dependency-check-report.json'
    project = project
    deps, vulns = get_dc_data.get_depcheck_data(project, file)
    if deps:
        print('[INFO] Ingesting the project name into Neo4J',flush=True)
        ingest_project(project)
        
        print('[INFO] Ingesting dependencies into Neo4J',flush=True)
        ingest_dependencies(deps, project)
        
        print('[INFO] Ingesting vulnerabilities',flush=True)
        ingest_vulns(vulns)
        
        print('[INFO] Creating relationships between vulnerabilities and dependencies',flush=True)
        create_vuln_relations()
        
        print('[INFO] Creating relationships between the dependencies and the project', flush=True)
        create_project_relations()

        print('[INFO] Adding colors to the vulnerabilities based on severity.', flush=True)
        add_label_colors()
        print("[INFO] Data successfully ingested in Neo4J",flush=True)
    else:
        print("[ERROR] No data has been ingested")
    driver.close() #Added to close the Driver

def ingest_project(project):
    '''
    Ingest the project into Neo4J
    '''
    tx.run('''
    MERGE (n:project {project_name: $project})
    ''', project=project)


def ingest_vulns(vulns_list):
    '''
    Ingest the vulnerabilities from the dependencies into Neo4J.
    '''
    tx.run('''    UNWIND $mapEntry AS mItem
              CALL apoc.merge.node(["vulnerability"],
              {vulnerability_name:mItem["CVE"],
              severity:mItem["CVSSv3"],
              severity_desc:mItem["severity_desc"]})
              YIELD node
              return node
            '''
           , mapEntry=vulns_list)


def ingest_dependencies(dependencies, project):
    '''
    Ingest the dependencies into Neo4J.
    '''
    for dependency in dependencies:
        r = tx.run('''
          MATCH (d:dependency {dependency: $dependency})
          return d
                 ''', dependency=dependency.get('dependency'))
        if r.single():
            tx.run('''
          MATCH (d:dependency {dependency: $dependency})
          WHERE NOT ($projects  IN d.projects)
          SET d.projects = d.projects + $projects
                 ''',
                   dependency=dependency.get('dependency'), projects=project)

            tx.run('''
          MATCH (d:dependency {dependency: $dependency})
          SET d.vulnerabilities = $vulnerabilities
          ''',
                   dependency=dependency.get('dependency'), vulnerabilities=dependency.get('vulnerabilities'))

        else:
            tx.run('''
            MERGE (d:dependency {package: $package, dependency: $dependency,
            vulnerabilities: $vulnerabilities, projects: $projects})
            ''', package=dependency.get('package'), dependency=dependency.get('dependency'),
                   vulnerabilities=dependency.get('vulnerabilities'), projects=dependency.get('project'))


def create_vuln_relations():
    '''
    Create the relationships between the dependencies
    and vulnerabilities in Neo4J.
    '''
    tx.run('''   MATCH (d:dependency), (v:vulnerability)
    WHERE v.vulnerability_name IN  d.vulnerabilities

    MERGE(d)-[:VULNERABLE_TO]->(v)
    ''')


def create_project_relations():
    '''
    Create the relationships between the dependencies and the project.
    '''
    r = tx.run('''
    MATCH (d:dependency), (p:project)
    WHERE p.project_name IN  d.projects
    MERGE (p)-[:USES]->(d)
    ''')

def add_label_colors():
    '''
    Adds colors to the nodes representing vulnerabilities based on
    severity level.
    '''
    tx.run('''
    MATCH (v:vulnerability)
    WITH DISTINCT v.severity_desc as severity_desc, collect(DISTINCT v) AS vulns
    CALL apoc.create.addLabels(vulns, [severity_desc]) YIELD node
    RETURN *
    ''')
