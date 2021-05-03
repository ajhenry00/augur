from pypi import get_lib_days, get_no_of_releases
from utils import load_requirements, get_requirement_files, get_requirement_name_and_version

class Libyear:

    def __init__(self, config={}):
        name = "libyear"
    
    def get_libyear(self, path):
        requirements = set()
        requirements_files = list(get_requirement_files(path))

        if len(requirements_files) != 0:

            for req_file in requirements_files:
                requirements.update(load_requirements(req_file))
       
            total_days = 0
    
            for req in requirements:
                name, version, version_lt = get_requirement_name_and_version(req)
                if not name:
                    continue

                if not version and not version_lt:
                    continue
        
                v, lv, days = get_lib_days(name, version, version_lt)
                total_days += days

            return round(total_days / 365, 2)
        else:
            return None
