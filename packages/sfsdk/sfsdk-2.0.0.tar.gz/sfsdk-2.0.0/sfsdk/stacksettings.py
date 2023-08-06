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
import json
import copy
import uuid
import tempfile

base_dir = None

stacks = {}

slug_components = [
    'technology',
    'variant'
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

    stacks[authsettings.current_source] = {}

    loaded_uuids = {} # To check duplicates
    for stack_yml_path in glob.glob('%s/stack/*/stack.yml' % base_dir):

        meta_name_by_folder = os.path.join(*stack_yml_path.split('/')[-3:-1])
        
        loaded_meta = load_stack_meta(meta_name_by_folder)

        meta_name_by_metadata = get_standard_stack_name(loaded_meta)

        # Do not consider meta-changed exercises as wrong
        if loaded_meta['uuid'] != 'xxxx' and meta_name_by_metadata != meta_name_by_folder:
            raise log.FatalMsg("Stack %s in incorrect folder %s" % (meta_name_by_metadata, stack_yml_path))

        if meta_name_by_metadata in stacks[authsettings.current_source].keys():
            raise log.FatalMsg("Local stack %s has a duplicate name" % (meta_name_by_metadata))
            
        if loaded_meta['uuid'] != 'xxxx' and loaded_meta['uuid'] in loaded_uuids:
            raise log.FatalMsg("Local stacks %s and %s have the same uuid" % (meta_name_by_metadata, loaded_uuids[loaded_meta['uuid']]))

        stacks[authsettings.current_source][meta_name_by_metadata] = loaded_meta
        loaded_uuids[loaded_meta['uuid']] = meta_name_by_metadata

def get_standard_stack_name(meta_data):

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

    return 'stack/%s-%s' % (
        slug,
        shorter_uuid
    )

def save_stack_meta(stack_yaml_orig):

    stack_yaml = copy.deepcopy(stack_yaml_orig)

    stack = get_standard_stack_name(stack_yaml)

    stack_dir = os.path.join(base_dir, stack)

    if not os.path.exists(stack_dir):
        os.makedirs(stack_dir)

    information_text = stack_yaml['md']['text']
    information_text = utils.save_and_replace_b64_with_media(
        base_folder = stack_dir,
        content = information_text,
        content_name = 'stack'
    )
    with open(os.path.join(stack_dir, 'stack.md'), 'w+') as f:
        f.write(information_text)
    stack_yaml['md']['text'] = '!import stack.md'

    reload_text = stack_yaml['mdReload'].get('text')
    if reload_text:

        reload_text = utils.save_and_replace_b64_with_media(
            base_folder = stack_dir,
            content = reload_text,
            content_name = 'reload'
        )
        with open(os.path.join(stack_dir, 'reload.md'), 'w+') as f:
            f.write(reload_text)
        stack_yaml['mdReload']['text'] = '!import reload.md'

    if log.verbose:
        stack_meta_debug_path = os.path.join(stack_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (stack_meta_debug_path))
        with open(stack_meta_debug_path, 'w') as f:
              json.dump(stack_yaml_orig, f, indent=4)

    with open(os.path.join(stack_dir, "stack.yml"), "w") as f:
        yaml.dump(stack_yaml, f, default_flow_style=False)

    return stack_dir

def load_stack_meta(stack):

    stack_dir = os.path.join(base_dir, stack)

    stack_meta_path = os.path.join(stack_dir, 'stack.yml')

    with open(stack_meta_path, 'r') as stream:
        try:
            stack_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise log.FatalMsg(exc)

        with open(os.path.join(stack_dir, 'stack.md'), 'r') as stream:
            stack_yaml['md']['text'] = utils.load_and_replace_media_with_b64(
                stack_dir,
                stream.read()
            )

        reload_md_path = os.path.join(stack_dir, 'reload.md')
        if os.path.exists(reload_md_path):
            with open(reload_md_path, 'r') as stream:
                stack_yaml['mdReload']['text'] = utils.load_and_replace_media_with_b64(
                    stack_dir,
                    stream.read()
                )
            stack_yaml['restart'] = True

    return stack_yaml

def get_stacks():

    return stacks[authsettings.current_source]

def get_stack_name_data_by_uuid(stack_uuid):

    return next(((n, d) for (n, d) in get_stacks().items() if d['uuid'] == stack_uuid), (None, None))

def copy_stack_folder(old_stack_dir, new_stack_data):
    new_stack_dir = save_stack_meta(new_stack_data)
    log.warn("Copied from %s to %s" % (utils.prettypath(old_stack_dir), utils.prettypath(new_stack_dir)))

def update_stack_folder(old_stack_dir, new_stack_data):

    new_stack_dir = save_stack_meta(new_stack_data)

    if old_stack_dir != new_stack_dir:
        utils.trash_file(old_stack_dir)
        log.warn("Moved from %s to %s" % (utils.prettypath(old_stack_dir), utils.prettypath(new_stack_dir)))

def delete_stack_by_uuid(stack_uuid):

    current_name, stack_data = get_stack_name_data_by_uuid(stack_uuid)
        
    current_folder = os.path.join(base_dir, current_name)

    if stack_data['uuid'] == stack_uuid:

        tempfolder = tempfile.mkdtemp()

        print("Moving %s to %s" % (current_folder, tempfolder))

        shutil.move(current_folder, tempfolder)

        return stack_uuid