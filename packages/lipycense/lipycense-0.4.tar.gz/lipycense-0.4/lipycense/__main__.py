import pkg_resources
import sys
import os

# needs to run in an envinronment on which all of the packages listed in requirements.txt are installed.


help =  """
        HELP:

        -V 
        Non verbose mode, only prints out found licenses, one line each.

        NOTES:

        This program needs to run in an envinronment on which all of the packages listed in requirements.txt are installed.

        """

LICENSE_NOT_FOUND  = 'LICENSENOTFOUND'


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_pkg_license(pkgname):

    pkgs = pkg_resources.require(pkgname)
    pkg = pkgs[0]

    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    for line in lines:
        if line.startswith('License:'):
            return line[9:]
    return LICENSE_NOT_FOUND


def get_licenses(pkg_names):
    return [get_pkg_license(pkg_name) for pkg_name in pkg_names]


def pgk_names_from_requirements(pathname):
     with open(pathname, "r") as f:
        pkgs = f.read()
        pkg_names = [pkg_name.split("==")[0] for pkg_name in pkgs.split("\n") if pkg_name != ""]
     return pkg_names

def licenses_from_requirements(pathname):
    pkg_names = pgk_names_from_requirements(pathname)
    return get_licenses(pkg_names)



if __name__ == "__main__":

    # print help
    if "--help" in sys.argv:
        print(help)
      
        exit(0)


    try:
        pathname = sys.argv[1]
    except:
        print(f"Correct usage:\npython3 {__name__.replace('__', '')}.py path/to/requirements.txt\nFor options use --help")
        exit(-1)
    

    if not os.path.isfile(pathname):
        print(f"Error: '{pathname}' is not a file!")
        exit(-1)

    licenses = licenses_from_requirements(pathname)
    

    licences_string = ""
    for license in set(licenses):
        licences_string+=f"{license}\n"

 
    # non-verbose mode:
    if "-V" in sys.argv:
        print(licences_string)
        exit(0)

    num_packages_required = len(pgk_names_from_requirements(pathname))
    print("LICENSE CHECKER:")
    print("tot num pkgs found in requirements:", num_packages_required)
    
    print("licenses found: ", len([l for l in licenses if l != LICENSE_NOT_FOUND]))

    print(licenses)
    if LICENSE_NOT_FOUND not in licenses:
        print(f"{colors.OKGREEN}found all licenses!{colors.ENDC}")
    else:
        print(f"{colors.FAIL}some licenses are missing!")
        print("pkgs with missing license:")
        print([key for key, val in dict(zip(pgk_names_from_requirements(pathname), licenses)).items() if val == LICENSE_NOT_FOUND])
        print(colors.ENDC)

    print(f"the licenses are:\n{licences_string}" )
    print("license dictionary:")
    print(dict(zip(pgk_names_from_requirements(pathname), licenses)))





