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

import re
import os
import glob
import shutil
import json
import tempfile
import base64
import copy
import uuid
from sfsdk import log, utils, authsettings
from ruamel import yaml
from pathlib import Path

base_status_messages = {
    'ok': '0',
    'solved': '0',
    'fixed': '0',
    'nok': '1',
    'not-solved': '1',
    'vulnerable': '1',
    'broken-functionality': '2',
    'broken-login': '2',
    'broken-webserver': '2',
    'broken': '2',
    'not-installed': '2'
}

slug_components = [
    'technology',
    'framework',
    'title'
]

base_dir = None
exrs = {}

def load(workspace_dir):

    global base_dir, exrs

    base_dir = os.path.join(
            workspace_dir,
            'srcs',
            authsettings.current_source
        )

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    exrs[authsettings.current_source] = {}

    for exr_yml_path in glob.glob('%s/exr/*/exercise.yml' % base_dir):

        meta_name_by_folder = os.path.join(*exr_yml_path.split('/')[-3:-1])
        
        loaded_meta = load_exercise_meta(meta_name_by_folder)

        meta_name_by_metadata = get_standard_exercise_name(loaded_meta)

        if meta_name_by_metadata in exrs[authsettings.current_source].keys():
            raise log.FatalMsg("Local exercise %s has a duplicate name" % (meta_name_by_metadata))
            
        exrs[authsettings.current_source][meta_name_by_metadata] = loaded_meta

def get_standard_exercise_name(meta_data):

    slug = '_'.join(re.sub(
            "[^a-z0-9]+",
            "_",
            str(meta_data[c].lower())
        ) for c in slug_components)

    long_uuid = meta_data['uuid']

    if long_uuid[:6] in ('local-', 'sfsdk-'):
        shorter_uuid = long_uuid[:10]
    else:
        shorter_uuid = long_uuid[:4]

    return 'exr/%s-%s' % (
        slug,
        shorter_uuid
    )

def get_standard_flag_filename(technology, flag_data):

    flag_name = flag_data['title'].lower()

    slug = re.sub(
        "[^a-zA-Z0-9]+",
        "_",
    flag_name)

    return 'flag_%s' % (slug)

def ls_exercises():

    return sorted(get_exercises().keys())

def get_exercises():

    return exrs[authsettings.current_source]

def get_exercise_name_data_by_uuid(exercise_uuid):

    return next(((n, d) for (n, d) in get_exercises().items() if d['uuid'] == exercise_uuid), (None, None))


def get_exercise_by_name(name):

    exercise_data = get_exercises().get(name)

    if exercise_data:
        return exercise_data
    else:
        raise log.FatalMsg('The exercise %s does not exist locally' % name)

def remove_exercise(exercise):

    exr_data = get_exercise_by_name(exercise)
        
    current_folder = os.path.join(base_dir, exercise)

    tempfolder = tempfile.mkdtemp()

    log.warn("Moving %s to %s" % (current_folder, tempfolder))

    shutil.move(current_folder, tempfolder)

    return exr_data['uuid']

def load_exercise_meta(exercise):

    exercise_dir = os.path.join(base_dir, exercise)

    if not os.path.exists(exercise_dir):
        os.makedirs(exercise_dir)

    exercise_meta_path = os.path.join(exercise_dir, 'exercise.yml')

    exercise_yaml = {}

    try:

        with open(exercise_meta_path, 'r') as stream:

            try:
                exercise_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise log.FatalMsg(exc)

            with open(os.path.join(exercise_dir, 'description.txt.md'), 'r') as stream:
                exercise_yaml['description'] = utils.load_and_replace_media_with_b64(
                    exercise_dir,
                    stream.read()
                )

            with open(os.path.join(exercise_dir, 'solution.md'), 'r') as stream:
                exercise_yaml['solution']['text'] = utils.load_and_replace_media_with_b64(
                    exercise_dir,
                    stream.read()
                )

            # Dirty validation on multiple flags with the same name
            added_flag_names = []

            for i, flag_yaml in enumerate(exercise_yaml['flags']):

                flag_name = get_standard_flag_filename(exercise_yaml['technology'], flag_yaml)

                if flag_name in added_flag_names:
                    raise log.FatalMsg("Error, flag %s with the same name detected" % (flag_name))

                added_flag_names.append(flag_name)

                # Dirty validation here
                if len(flag_yaml['flagList']) > 1:
                    raise log.FatalMsg("Error, more than one flagList per flag")

                flaglist = flag_yaml['flagList'][0]

                flaglist_md_path = '%s.md' % (flag_name)

                with open(os.path.join(exercise_dir, flaglist_md_path), 'r') as stream:
                    exercise_yaml['flags'][i]['flagList'][0]['md']['text'] = utils.load_and_replace_media_with_b64(
                        exercise_dir,
                        stream.read()
                    )

                if 'hint' in flaglist and 'text' in flaglist['hint']['md']:
                    flaglist_hint_md_path = '%s_hint.md' % (flag_name)

                    with open(os.path.join(exercise_dir, flaglist_hint_md_path), 'r') as stream:
                        exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text'] = utils.load_and_replace_media_with_b64(
                            exercise_dir,
                            stream.read()
                        )

                if exercise_yaml.get('labType') in ( '1', 'CODE_REVIEW'):

                    with open(os.path.join(exercise_dir, '%s_lines.yml' % (flag_name)), "r") as f:

                        try:
                            crlines = yaml.safe_load(f)
                        except yaml.YAMLError as exc:
                            raise log.FatalMsg(exc)

                        exercise_yaml['flags'][i]['flagList'][0]['crVulns'] =  crlines.get('crVulns', [])

                if flaglist.get('selfCheckAvailable'):
                    
                    with open(os.path.join(exercise_dir, '%s_messages.yml' % (flag_name)), "r") as f:

                        try:
                            messages_yaml = yaml.safe_load(f)
                        except yaml.YAMLError as exc:
                            raise log.FatalMsg(exc)

                        exercise_yaml['flags'][i]['flagList'][0]['selfCheck']['messageMappings'] = {}
                        exercise_yaml['flags'][i]['flagList'][0]['selfCheck']['statusMapping'] = {}

                        if messages_yaml and type(messages_yaml) is dict:
                            for status_name, status_message in messages_yaml.items():

                                # Do not add if loaded status name is a base status message
                                if status_name in base_status_messages:
                                    continue

                                # Add only if loaded status name starts with a base status message
                                base_status_number = next((v for m,v in base_status_messages.items() if status_name.startswith(m + '-')), None)
                                if base_status_number == None:
                                    raise log.FatalMsg("Can't map message status '%s' on a basic status type" % (status_name))

                                exercise_yaml['flags'][i]['flagList'][0]['selfCheck']['messageMappings'][status_name] = status_message
                                exercise_yaml['flags'][i]['flagList'][0]['selfCheck']['statusMapping'][status_name] = base_status_number
                        
    except FileNotFoundError as e:
        raise log.FatalMsg(f"Can't load the metadata: {e.filename} was expected but not found.")

    return exercise_yaml

def save_exercise_meta(exercise_yaml_orig):

    exercise_yaml = copy.deepcopy(exercise_yaml_orig)

    exercise = get_standard_exercise_name(exercise_yaml)

    exercise_dir = os.path.join(base_dir, exercise)

    if not os.path.exists(exercise_dir):
        os.makedirs(exercise_dir)

    if log.verbose:
        exercise_meta_debug_path = os.path.join(exercise_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (exercise_meta_debug_path))
        with open(exercise_meta_debug_path, 'w') as f:
              json.dump(exercise_yaml, f, indent=4)

    description = exercise_yaml['description']
    description = utils.save_and_replace_b64_with_media(
        base_folder = exercise_dir,
        content = description,
        content_name = 'description'
    )
    with open(os.path.join(exercise_dir, 'description.txt.md'), 'w+') as stream:
        stream.write(description)

    exercise_yaml['description'] = '!import description.txt.md'

    solution_text = exercise_yaml['solution']['text']
    solution_text = utils.save_and_replace_b64_with_media(
        base_folder = exercise_dir,
        content = solution_text,
        content_name = 'solution'
    )
    with open(os.path.join(exercise_dir, 'solution.md'), 'w+') as stream:
        stream.write(solution_text)

    exercise_yaml['solution']['text'] = '!import solution.md'

    # Do not store the complete stack KB, but only variant and technology
    try:
        exercise_yaml['stack'] = {
            'technology' : exercise_yaml['stack']['technology'],
            'variant': exercise_yaml['stack']['variant'],
            'uuid': exercise_yaml['stack']['uuid']
        }
    except KeyError as e:
        raise log.FatalMsg(f"Metadata parsing error {e}")


    # Dirty validation on multiple flags with the same name
    added_flag_names = []

    for i, flag_yaml in enumerate(exercise_yaml['flags']):

        flag_name = get_standard_flag_filename(exercise_yaml['technology'], flag_yaml)

        if flag_name in added_flag_names:
            raise log.FatalMsg("Error, flag %s with the same name detected" % (flag_name))
        added_flag_names.append(flag_name)

        try:
            # Do not store the complete vulnerability KB, but only category, vulnerability, technology, and isAgnostic
            exercise_yaml['flags'][i]['kb'] = {
                'category' : exercise_yaml['flags'][i]['kb']['category'],
                'vulnerability': exercise_yaml['flags'][i]['kb']['vulnerability'],
                'technology': exercise_yaml['flags'][i]['kb']['technology'],
                'isAgnostic': exercise_yaml['flags'][i]['kb']['isAgnostic'],
                'uuid': exercise_yaml['flags'][i]['kb']['uuid']
            }
        except KeyError as e:
            raise log.FatalMsg(f"Metadata parsing error {e}")

        # Dirty validation on multiple flagList
        if len(flag_yaml['flagList']) > 1:
            raise log.FatalMsg("Error, more than one flagList per flag")

        flaglist = flag_yaml['flagList'][0]
            
        flaglist_md = flaglist['md']['text']
        flaglist_md_path = '%s.md' % (flag_name)

        flaglist_md = utils.save_and_replace_b64_with_media(
            base_folder = exercise_dir,
            content = flaglist_md,
            content_name = flag_name
        )

        with open(os.path.join(exercise_dir, flaglist_md_path), 'w+') as stream:
            stream.write(flaglist_md)

        exercise_yaml['flags'][i]['flagList'][0]['md']['text'] = '!import %s' % flaglist_md_path

        if 'hint' in flaglist and 'text' in flaglist['hint']['md']:
            flaglist_hint_md = flaglist['hint']['md']['text']
            flaglist_hint_md_path = '%s_hint.md' % (flag_name)

            flaglist_hint_md = utils.save_and_replace_b64_with_media(
                base_folder = exercise_dir,
                content = flaglist_hint_md,
                content_name = f'{flag_name}_hint'
            )

            with open(os.path.join(exercise_dir, flaglist_hint_md_path), 'w+') as stream:
                stream.write(flaglist_hint_md)

            exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text'] = '!import %s' % flaglist_hint_md_path

        if flaglist.get('selfCheckAvailable'):
            with open(os.path.join(exercise_dir, "%s_messages.yml" % (flag_name)), "w") as f:
                yaml.dump(flaglist['selfCheck']['messageMappings'], f, default_flow_style=False, width=float("inf"))
                exercise_yaml['flags'][i]['flagList'][0]['selfCheck']['messageMappings'] = "!import %s_messages.yml" % (flag_name)
        
        if exercise_yaml.get('labType') in ( '1', 'CODE_REVIEW'):

            with open(os.path.join(exercise_dir, '%s_lines.yml' % (flag_name)), "w+") as f:

                yaml.dump({
                    'crVulns': flaglist['crVulns'],
                }, f, default_flow_style=False, width=float("inf"))

                exercise_yaml['flags'][i]['flagList'][0]['crVulns'] = '!import %s_lines.yml crVulns' % (flag_name)

    fix_incoming_exercise_data(exercise_yaml)

    with open(os.path.join(exercise_dir, "exercise.yml"), "w") as f:
        yaml.dump(exercise_yaml, f, default_flow_style=False, width=float("inf"))

    return exercise_dir

def copy_exercise_folder(old_exercise_dir, new_exercise_data):

    new_exercise_dir = save_exercise_meta(new_exercise_data)
    log.warn("Copied from %s to %s" % (utils.prettypath(old_exercise_dir), utils.prettypath(new_exercise_dir)))

def update_exercise_folder(old_exercise_dir, new_exercise_data):

    new_exercise_dir = save_exercise_meta(new_exercise_data)

    if old_exercise_dir != new_exercise_dir:
        utils.trash_file(old_exercise_dir)
        log.warn("Moved from %s to %s" % (utils.prettypath(old_exercise_dir), utils.prettypath(new_exercise_dir)))


def get_exercise_environment_variable(exercise_name):

    exercise_settings = get_exercise_by_name(exercise_name)
    return base64.b64encode(json.dumps(
            {
                'title': exercise_settings['title'],
                'flags': exercise_settings['flags']
            }
        ).encode()
    )

def generate_exercise_environment(flag_name):

    return base64.b64encode(json.dumps(
            {
                'flags': [{"flagList":[{"selfCheck":{"name": flag_name }}]}]
            }
        ).encode()
    )

def fix_incoming_exercise_data(exercise_json):

    # Int-ify status
    exercise_json['status'] = int(exercise_json['status'])

    # Sort by flag type, to keep always the same order
    exercise_json['flags'].sort(key=lambda f: f['flagList'][0]['type'])

    # Delete ids
    utils.recursive_del(exercise_json['flags'], 'id')
    
    try:
        del exercise_json['solution']['id']
    except KeyError:
        pass

    # Map labType to strings
    labType = exercise_json.get('labType')
    if not labType or labType == '0':
        exercise_json['labType'] = 'LAB'
    elif labType == '1':
        exercise_json['labType'] = 'CODE_REVIEW'
    elif labType == '2':
        exercise_json['labType'] = 'QUIZ'

def fix_outgoing_exercise_data(exercise_json):

    # Int-ify status
    exercise_json['status'] = int(exercise_json['status'])

    # Delete any reference to KBs and Stack UUIDs, let the platform guess by other meta
    utils.recursive_del(exercise_json['flags'], 'uuid')
    utils.recursive_del(exercise_json['stack'], 'uuid')

    # Delete md.id in flags that cause some issue
    utils.recursive_del(exercise_json['flags'], 'id')

    # Map labType to strings
    labType = exercise_json.get('labType')
    if not labType or labType == '0':
        exercise_json['labType'] = 'LAB'
    elif labType == '1':
        exercise_json['labType'] = 'CODE_REVIEW'
    elif labType == '2':
        exercise_json['labType'] = 'QUIZ'

def get_path(exercise_name):
   return os.path.join(base_dir, exercise_name)

def get_pretty_path(exercise_name):
   return utils.prettypath(os.path.join(base_dir, exercise_name))