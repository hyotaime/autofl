from lib.d4j_interface import D4JRepositoryInterface

D4J_PROJECTS = [
    'Chart',
    'Cli',
    'Closure',
    'Codec',
    'Collections',
    'Commons-io',
    'Compress',
    'Csv',
    'Gson',
    'JacksonCore',
    'JacksonDatabind',
    'JacksonXml',
    'Jsoup',
    'JxPath',
    'lang',
    'Lang',
    'Math',
    'Mockito',
    'Time',
]


def get_repo_interface(bug_name, **ri_kwargs):
    def _name_matches_proj_list(name, proj_list):
        return any(name.lower() == proj_name.lower()
                   for proj_name in proj_list)
    proj, bug_num = bug_name.split('_')
    if _name_matches_proj_list(proj, D4J_PROJECTS):
        return D4JRepositoryInterface(bug_name, **ri_kwargs)
    else:
        raise ValueError(f'Unknown project {proj} detected from {bug_name}.')
