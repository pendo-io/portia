
## Installation Options & Running Neosource

This program offers three different options for implementing Neo4J for this project.

If you are not running this on Docker, be sure the environment you are running it on has [Java](https://www.java.com/en/download/manual.jsp "https://www.java.com/en/download/manual.jsp") installed as DepedencyCheck requires it to run.

### Download Neosource From Github

Download your platform’s version of Neosource from the [GitHub releases page](https://github.com/SamDeAngelis/portia/releases "https://github.com/SamDeAngelis/portia/releases") (or the Docker release if you prefer to use that instead). If using the Docker version, go to the Docker section below. Make sure to move the downloaded release to a more permanent location where you won’t accidentally delete the project (i.e., not in a Downloads folder). Once it is downloaded you need to add the program to your system’s Path environment variable.

#### Add Neosource to Windows Path Variable

1.  Open Control Panel.
    
2.  In the search bar, input “environment variable”.
    
3.  Click “Edit the system variables”.
    
4.  When asked “Do you want to allow this app to make changes on your computer?” select “Yes”.
    
5.  Select “Environment Variables…” on the System Properties.
    
6.  Under the “System Variables”, select “Path” and click “Edit”.
    
7.  Click “New”.
    
8.  Add in the absolute path of neosource.bat.
    

#### Add Neosource to Linux/macOS Path Variable

1.  Open one of the following files in your favorite text editor (depending on your shell type): ~/.bash_profiile, ~/.bashrc, ~/.profile, ~/.kshrc, or ~/.zshrc.
    
2.  Add the following to the end of the file
    
    `export PATH=$PATH:[path to neosource.sh]`
    
3.  Save the file and exit.
    

### Set Up config.in

1.  Locate the config.in file found at (provide path to the config.in file).
    
2.  Open this file using a text editor.
    
3.  Change the value of the password to the one you wish to use for your program and the DB to the IP address of where the data will be stored (if running locally, can just use “localhost:7687” as the address).
    

### Setting Credentials

If you are accessing your Neo4J instance for the first time, you need to go to the address specified in config.in on port 7474 (i.e., if you chose to use localhost as your address, you should navigate to localhost:7474). From there you should log in with the default credentials (neo4j, neo4j) in order to be able to change the credentials. Be sure to change your password to the one specified in your config.in.

### Existing/Local Neo4J

#### Access An Existing Neo4J Instance:

Note: requires you to know the connection information (IP address and port) of an existing Neo4J instance.

#### Use Neo4J Desktop

The first option is to download the desktop version of Neo4J from the website listed below:

Now you need to set up your credentials for Neo4J.

Once Neo4J is running, you need to go to a project’s database (or create a project) and go to the Plugins tab and install Apoc.

Once you have your config.in file set up, and you have logged into Neo4J to properly [set your credentials](https://trwilcox.atlassian.net/wiki/spaces/CYBERSECPE/pages/1704097#Setting-Credentials "https://trwilcox.atlassian.net/wiki/spaces/CYBERSECPE/pages/1704097#Setting-Credentials"), you can run the program as follows:

#### Windows

`./neosource.exe [directory/file to scan] #If you want to use the default project name`</br>
`./neosource.exe -p [project name] [directory/file to scan] #If you have a project name`

#### Linux

`./neosource.sh [directory/file to scan] #If you want to use the default project name`</br>
`./neosource.sh -p [project name] [directory/file to scan] #If you have a project name`

#### MacOS

`./neosource.sh [directory/file to scan] #If you want to use the default project name`</br>
`./neosource.sh -p [project name] [directory/file to scan] #If you have a project name`

If this is the first time you’ve run neosource on your machine, or if DependencyCheck has an update to its database, the program will take longer to run as it will download updates of CVE’s to look for.

Otherwise, the output should look something like this:
```
[INFO] [filepath]
[INFO] Validating neo4j instance
[INFO] A valid NEO4J existence!
[INFO] Starting dependency-check: 
# A bunch of logs from DependencyCheck running …
[INFO] Validating JSON file 
[INFO] No Exception thrown by dependency-check
[INFO] Ingesting the project name into Neo4J
[INFO] Ingesting dependencies into Neo4J
[INFO] Ingesting vulnerabilities
[INFO] Creating relationships between vulnerabilities and dependencies
[INFO] Creating relationships between the dependencies and the project
[INFO] Adding colors to the vulnerabilities based on severity.
[INFO] Data successfully ingested in Neo4J
[INFO] Removing json file
[INFO] Open up Neo4J to view results. http://localhost:7474/
[INFO] Run the query 'MATCH (n) RETURN n' to view all results
```
### Use the Docker Version of Neosource

The second option requires you to have Docker installed ( ) along with the repository containing your config.in, the Dockerfile, get_dc_data.py, ingest_data_neo4j.py, neosource.py. Be sure to [set up your config.in](https://trwilcox.atlassian.net/wiki/spaces/CYBERSECPE/pages/1704097/User+Installation+Guide#Set-Up-config.in "https://trwilcox.atlassian.net/wiki/spaces/CYBERSECPE/pages/1704097/User+Installation+Guide#Set-Up-config.in") before continuing. In the Dockerfile, change the NEO4J_AUTH environment variable’s value to be neo4j/[the password you set in config.in]

In the directory including all of the necessary files, run the following commands:

`docker build -t neosource . docker run -dp 7474:7474 -p 7687:7687 neosource`

**Note: you may need to use sudo if running from Linux**

Be sure to wait a minute or two before moving on as the container spins up. At this point you need to go to the address you specified as NEO4J_DB in config.in (note: because of how the base Docker image for Neo4J works, you will be able to skip the step of setting your credentials).

Back on the command line, run the following:

`docker ps`</br>
`docker cp [path to directory you want to scan or file you want scanned] [docker image id]:/var/lib/neo4j`</br>
`docker exec -it [docker container id] python3 neosource.py [directory/file you specified in the previous command]`

Alternatively, can run the program with

`docker exec -it [docker container id] python3 neosource.py -p [project name] [directory/file you specified in the previous command]`

You should see output that looks something like this:

```
[INFO] [Path to file]
[INFO] Validating neo4j instance
[INFO] A valid NEO4J existence!
[INFO] Starting dependency-check: #A bunch of logs from DependencyCheck running …
[INFO] Validating JSON file
[INFO] No Exception thrown by dependency-check
[INFO] Ingesting the project name into Neo4J
[INFO] Ingesting dependencies into Neo4J
[INFO] Ingesting vulnerabilities
[INFO] Creating relationships between vulnerabilities and dependencies
[INFO] Creating relationships between the dependencies and the project
[INFO] Adding colors to the vulnerabilities based on severity.
[INFO] Data successfully ingested in Neo4J
[INFO] Removing json file
[INFO] Open up Neo4J to view results. http://localhost:7474/
[INFO] Run the query 'MATCH (n) RETURN n' to view all results
```

### Checking Results in Neo4J

Regardless of the method chosen for running the program, you should navigate to your instance of Neo4J (if you chose to use localhost as your address while setting up your config.in file, you should navigate to localhost:7474). From there, you should refresh the page and then run

`MATCH(n) RETURN(n);`

This will show you all of the dependencies for all of the projects in the system.

If you have multiple projects in your instance of Neo4J, you can run the following command to specify just the nodes for this specific project:

`MATCH(a:dependency), (v:vulnerability), (m:project) WHERE m.project_name="[project name given to neosource or 'project' if no project name specified]" RETURN a,v,m;`

### FAQ

-   What platforms does this project run on?
    
    -   The current platforms that are supported are Linux, MacOS, and Windows.
        
-   What types of files is this capable of scanning?
    
    -   Currently, the program is capable of scanning go.mod/go.sum, requirements.txt, and package.json/package-lock.json files. We built this program expressly for these dependencies, but it could be changed to accommodate [other types of dependencies](https://jeremylong.github.io/DependencyCheck/analyzers/index.html "https://jeremylong.github.io/DependencyCheck/analyzers/index.html"), so long as DepdencyCheck is capable of scanning them.
        
-   Which dependencies do I have to install?
    
    -   Java and Go Lang.
        
-   What types of inputs do I need to provide for this program?
    
    -   A properly set up config.in, as described above, and command-line arguments, as described above, and the Dockerfile, if using Docker.
        

### Troubleshooting

#### Scanning Python Dependencies

To scan for Python dependencies you can specify either the path to the directory housing requirements.txt or the specific path to it.

#### Scanning Javascript Dependencies

To scan for Javascript dependencies you need to specify the path to the repository housing package.json AND package-lock.json. If you are using the Docker version, we recommend that you copy the entire repository to the Docker container, but it may still work with just the two individual files if you find that the repository is too large.

#### Scanning Go Lang Dependencies

To scan for Go Lang dependencies you need to specify the path to go.mod or the repository that contains go.mod being sure that go.sum is in the same repository context as go.mod.

#### Program Not Accepting My Credentials

If you are not using the Docker version, you need to set up your credentials in Neo4J before you can run the program. If you have the username/password combo of neo4j/neo4j, you need to change your password.

#### Issue With Running DependencyCheck In Neosource

For Linux and macOS users, dependency-check.sh should be executable upon download. If, however, it isn’t for some reason, you can make it executable by doing the following in dependency-check/bin:

`chmod +x dependency-check.sh chmod +x completion-for-dependency-check.sh`

#### My DependencyCheck Threw An Error Downloading NVD

Re-run neosource, as this will likely fix the issue.

### Known Issues

-   Be careful to input your credentials correctly. Neo4J will lock you out after a couple of incorrect attempts.
    
-   Python and Go Lang are listed under DependencyCheck’s “Experimental Analyzers” meaning that they have a higher rate of false positives and false negatives, so any scans involving these dependencies should be carefully scrutinized.
    
-   The version of DependencyCheck that is bundled with the non-Docker versions of neosource may not be the latest version.
    
-   The version of Go lang bundled with the Docker version of neosource will most likely not be the latest version. You may want to update it in the container yourself. To do this, refer to the documentation for [Go lang](https://go.dev/doc/install "https://go.dev/doc/install").
