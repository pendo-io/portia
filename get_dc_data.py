import json
import urllib


def get_identifiers(identifiers):
    info = {}

    # no packages
    if 'packages' not in identifiers:
        info['package'] = '-'
        info['dependency'] = '-'
        info['project'] = '-'
        info['application'] = '-'
        return info

    package = identifiers['packages'][0]['id'].split('/')
    info['package'] = package[0].split(':')[1]

    if info['package'] == 'maven':
        dependency = package[1] + '.' + package[2]
        info['dependency'] = dependency
        info['project'] = package[1]
        info['application'], info['version'] = package[2].rsplit('@', 1)

    elif info['package'] == 'javascript':
        info['project'] = '-'
        info['application'], info['version'] = package[1].rsplit('@', 1)
        info['dependency'] = package[0] + '.' + package[1]

    elif info['package'] == 'npm':
        package[1] = urllib.parse.unquote(package[1])
        info['project'] = '-'
        info['dependency'] = package[0] + '/' + package[1]
        try:
            info['application'], info['version'] = package[1].rsplit('@', 1)
        except ValueError:
            info['application'] = package[1]
            info['version'] = '-'

    elif info['package'] == 'golang':
        info['project'] = '-'
        info['dependency'] = identifiers['packages'][0]['id'].split('/', 1)[1]
        try:
            info['application'], info['version'] = info['dependency'].rsplit('@', 1)
        except ValueError:
            info['application'] = info['dependency']
            info['version'] = '-'
    else:
        info['project'] = package[1]
        info['dependency'] = package[0] + '.' + package[1]

    return info


def get_vulnerabilities_data(vulnerabilities):
    info = []
    cve_list = []
    for vulnerability in vulnerabilities:
        vuln_info = {}
        vuln_info['CVE'] = vulnerability['name']
        if vulnerability['name'] not in cve_list:
            cve_list.append(vulnerability['name'])
        try:
            vuln_info['CVSSv3'] = float(vulnerability['cvssv3']['baseScore'])
            vuln_info['severity_desc'] = vulnerability['cvssv3']['baseSeverity']
        except KeyError:
            vuln_info['CVSSv3'] = 0.0
            vuln_info['severity_desc'] = "None"
        info.append(vuln_info.copy())
    return info, cve_list


def get_dc_data(dependencies, project):
    dependency_list = []
    vuln_list = []
    for dependency in dependencies:
        dependency_data = get_identifiers(dependency)
        dependency_data['project'] = [project]
        dependency_data['vulnerabilities'] = []
        if 'vulnerabilities' in dependency:
            vuln_data, cves = get_vulnerabilities_data(dependency['vulnerabilities'])
            vuln_list = vuln_list + vuln_data
            dependency_data['vulnerabilities'] = cves
        if dependency_data.copy() not in dependency_list:
            dependency_list.append(dependency_data.copy())

    return dependency_list, vuln_list


def get_depcheck_data(project, file):
    try:
        with open(file) as f:
            dependencies = json.loads(f.read()).get('dependencies')
            return get_dc_data(dependencies, project)

    except FileNotFoundError:
        print("[ERROR] File {} not found".format(file))
        return None, None
