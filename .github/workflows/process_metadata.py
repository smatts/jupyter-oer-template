import os
import sys
import yaml

config_filename = '_config.yml'
metadata_filename = 'metadata.yml'

if not os.path.exists(metadata_filename):
    print('Metadata file does not exist. Please add a ' + metadata_filename + ' file.')
    sys.exit(1)

if not os.path.exists(config_filename):
    print('Config file ' + config_filename + ' does not exist. Was it deleted?')
    sys.exit(1)

# Get metadata and config files
with open(metadata_filename, 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
with open(config_filename, 'r') as config_file:
    config = yaml.safe_load(config_file.read())

# Get branch
branch = None
if os.path.exists('branch.txt'):
    with open('branch.txt', 'r') as f:
        branch = f.read().strip()

def build_author(creator):
    # This only takes the first creator, as Jupyter Books only have one author.
    if 'givenName' in creator[0] and 'familyName' in creator[0]:
        return creator[0]['givenName'] + ' ' + creator[0]['familyName']
    return None


replace_values = {
    'title': metadata['name'] if 'name' in metadata else None,
    'author': build_author(metadata['creator']) if 'creator' in metadata else None,
    'repository': {
        'url': metadata['url'] if 'url' in metadata else config['repository']['url'],
        'branch': branch or config['repository']['branch'],
    },
    'logo': metadata['image'] if 'image' in metadata else None
}

new_config_filename = "_config_gen.yml"
with open(new_config_filename, 'w') as new_config:
    for key in config.keys():
        if key in replace_values and replace_values[key]:
            yaml.safe_dump({key: replace_values[key]}, new_config)
        else:
            yaml.safe_dump({key: config[key]}, new_config)

os.rename(new_config_filename, config_filename)
