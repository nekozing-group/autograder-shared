from importlib import resources
import tomllib

def iter_toml():
    # Using files() to get a Traversable object of the directory
    with resources.files('shared.data') as resource_dir:
        for resource in resource_dir.iterdir():
            # Check if it's a file and not a directory
            if resource.is_file() and resource.suffix == '.toml':
                # Read the content of the file
                with resources.as_file(resource) as resource_file:
                    with open(resource_file, 'r', encoding='utf-8') as file:
                        toml = tomllib.loads(file.read())
                        yield resource_file.name, toml

def test_schema():
    for _, toml in iter_toml():
        assert type(toml['testcases']) == list
        metadata = toml['metadata']
        assert all(key in metadata for key in ['entrypoint', 'user_template', 'problem_description', 'reference_implementation'])
    

def test_reference_impl():
    filename = None
    try:
        for name, toml in iter_toml():
            filename = name
            code = toml['metadata']['reference_implementation']
            byte_code = compile(code, '<inline>', 'exec')
            loc = {}
            glob = {}
            exec(byte_code, glob, loc)
            loc = loc | glob
            for testcase in toml['testcases']:
                input, expected_output = testcase['input'], testcase['expected_output']
                assert expected_output == loc[toml['metadata']['entrypoint']](input)
    except Exception as e:
        raise AssertionError(f'{filename} - {type(e).__name__} - {str(e)}')
