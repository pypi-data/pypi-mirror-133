# This file is part of the SecureFlag Platform.
# Copyright (c) 2022 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import exrsettings, log, utils, authsettings
from ruamel import yaml
import os
import shutil
import glob
import re
import shutil
import json
import copy
import tempfile

base_dir = None

kbs = {}

slug_components = [
    'technology',
    'vulnerability'
]

def load(workspace_dir):

    global base_dir, exrs

    base_dir = os.path.join(
            workspace_dir,
            'srcs',
            authsettings.current_source
        )

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    kbs[authsettings.current_source] = {}

    for kb_yml_path in glob.glob('%s/kb/*/kb.yml' % base_dir):

        meta_name_by_folder = os.path.join(*kb_yml_path.split('/')[-3:-1])
        
        loaded_meta = load_kb_meta(meta_name_by_folder)

        meta_name_by_metadata = get_standard_kb_name(loaded_meta)

        if meta_name_by_metadata in kbs[authsettings.current_source].keys():
            raise log.FatalMsg("Local kb %s has a duplicate name" % (meta_name_by_metadata))
            
        kbs[authsettings.current_source][meta_name_by_metadata] = loaded_meta

def get_standard_kb_name(meta_data):

    slug = '_'.join(re.sub(
            "[^a-z0-9]",
            "_",
            str(meta_data[c].lower())
        ) for c in slug_components)

    long_uuid = meta_data['uuid']

    if long_uuid[:6] in ('local-', 'sfsdk-'):
        shorter_uuid = long_uuid[:10]
    else:
        shorter_uuid = long_uuid[:4]

    return 'kb/%s-%s' % (
        slug,
        shorter_uuid
    )

def save_kb_meta(kb_yaml_orig):

    kb_yaml = copy.deepcopy(kb_yaml_orig)

    kb = get_standard_kb_name(kb_yaml)

    kb_dir = os.path.join(base_dir, kb)

    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)


    information_text = kb_yaml['md']['text']
    information_text = utils.save_and_replace_b64_with_media(
        base_folder = kb_dir,
        content = information_text,
        content_name = 'kb'
    )
    with open(os.path.join(kb_dir, 'kb.md'), 'w+') as f:
        f.write(information_text)
    kb_yaml['md']['text'] = '!import kb.md'

    if log.verbose:
        kb_meta_debug_path = os.path.join(kb_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (kb_meta_debug_path))
        with open(kb_meta_debug_path, 'w') as f:
              json.dump(kb_yaml_orig, f, indent=4)

    with open(os.path.join(kb_dir, "kb.yml"), "w") as f:
        yaml.dump(kb_yaml, f, default_flow_style=False)

    return kb_dir

def load_kb_meta(kb):

    kb_dir = os.path.join(base_dir, kb)

    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)

    kb_meta_path = os.path.join(kb_dir, 'kb.yml')

    kb_yaml = {}

    try:

        with open(kb_meta_path, 'r') as stream:
            try:
                kb_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise log.FatalMsg(exc)

            with open(os.path.join(kb_dir, 'kb.md'), 'r') as stream:
                kb_yaml['md']['text'] = utils.load_and_replace_media_with_b64(
                        kb_dir,
                        stream.read()
                    )

            

    except IOError:
        pass

    return kb_yaml

def get_kbs():

    return kbs[authsettings.current_source]

def get_kb_name_data_by_uuid(kb_uuid):
    
    return next(((n, d) for (n, d) in get_kbs().items() if d['uuid'] == kb_uuid), (None, None))


def delete_kb_by_uuid(kb_uuid):

    current_name, kb_data = get_kb_name_data_by_uuid(kb_uuid)
        
    current_folder = os.path.join(base_dir, current_name)

    if kb_data['uuid'] == kb_uuid:

        tempfolder = tempfile.mkdtemp()

        log.warn("Moving %s to %s" % (current_folder, tempfolder))

        shutil.move(current_folder, tempfolder)

        return kb_uuid

def copy_kb_folder(old_kb_dir, new_kb_data):
    new_kb_dir = save_kb_meta(new_kb_data)
    log.warn("Copied from %s to %s" % (utils.prettypath(old_kb_dir), utils.prettypath(new_kb_dir)))

def update_kb_folder(old_kb_dir, new_kb_data):

    new_kb_dir = save_kb_meta(new_kb_data)

    if old_kb_dir != new_kb_dir:
        utils.trash_file(old_kb_dir)
        log.warn("Moved from %s to %s" % (utils.prettypath(old_kb_dir), utils.prettypath(new_kb_dir)))
