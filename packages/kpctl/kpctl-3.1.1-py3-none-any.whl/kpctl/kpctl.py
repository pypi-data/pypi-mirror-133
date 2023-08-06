#!/usr/bin/python3
###############################################################################
# Copyright 2015-2022 Tim Stephenson and contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Command line client for managing process application lifecycle.
#
###############################################################################
import argparse
import base64
from cairosvg import svg2png
import configparser
from configparser import ConfigParser
import colorama
from colorama import Fore, Back, Style
from enum import Enum, unique
from getpass import getpass
import glob
import kpctl
import lxml.etree as ET
from oauthlib.oauth2 import LegacyApplicationClient
import os
from os.path import basename
from os.path import exists
from os import mkdir
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import shutil
import sys
import urllib.request
import urllib.parse
from xml.dom.minidom import parseString
from zipfile import ZipFile

APP_NAME = 'KnowProcess Modeler'
APP_VSN = '3.1'

TEMPLATE_APP_DESCRIPTOR = '''{
  "key": "%s",
  "name": "%s",
  "description": "",
  "theme": "theme-10",
  "icon": "glyphicon-plus",
  "usersAccess": null,
  "groupsAccess": null
}
'''
TEMPLATE_FORM = '''{
  "key": "%s",
  "name": "%s",
  "version": 0,
  "fields": [%s
  ],
  "outcomes": []
}
'''
TEMPLATE_FORM_FIELD = '''
    {
      "fieldType": "FormField",
      "id": "%s",
      "name": "%s",
      "type": "text",
      "value": null,
      "required": false,
      "readOnly": false,
      "overrideId": true,
      "placeholder": "",
      "layout": null
    }'''
CACHE_DIR = os.path.expanduser('~') + '/.kp'
BPMN_XSD_ROOT_PATH = CACHE_DIR + '/xsd/BPMN20.xsd'

XSD_BPMN = 'http://modeler.knowprocess.com/xsd/BPMN20.xsd'
XSD_BPMNDI = 'http://modeler.knowprocess.com/xsd/BPMNDI.xsd'
XSD_DC = 'http://modeler.knowprocess.com/xsd/DC.xsd'
XSD_DI = 'http://modeler.knowprocess.com/xsd/DI.xsd'
XSD_SEMANTIC = 'http://modeler.knowprocess.com/xsd/Semantic.xsd'
XSLT_VALIDATOR = 'http://modeler.knowprocess.com/xslt/bpmn2issues.xslt'
XSLT_EXT_VALIDATOR = 'http://modeler.knowprocess.com/xslt/bpmn2flowableissues.xslt'
XSLT_PROC_RENDERER = 'http://modeler.knowprocess.com/xslt/bpmn2svg.xslt'
XSLT_PROC_ENHANCER = 'http://modeler.knowprocess.com/xslt/bpmn2executable.xslt'

NS = {
    'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
    'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
    'bpsim': 'http://www.bpsim.org/schemas/1.0',
    'color': 'http://www.omg.org/spec/BPMN/non-normative/color/1.0',
    'di': 'http://www.omg.org/spec/DD/20100524/DI',
    'dc': 'http://www.omg.org/spec/DD/20100524/DC',
    'dmn': 'http://www.omg.org/spec/DMN/20180521/MODEL/',
    'dmn12': 'http://www.omg.org/spec/DMN/20180521/MODEL/',
    'feel': 'https://www.omg.org/spec/DMN/20191111/FEEL/',
    'i18n': 'http://www.omg.org/spec/BPMN/non-normative/extensions/i18n/1.0',
    'activiti': 'http://activiti.org/bpmn',
    'camunda': 'http://camunda.org/schema/1.0/bpmn',
    'drools': 'http://www.jboss.org/drools',
    'flowable': 'http://flowable.org/bpmn',
    'html': 'http://www.w3.org/1999/xhtml',
    'kp': 'http://knowprocess.com/bpmn',
    'openapi': 'https://openapis.org/omg/extension/1.0',
    'rss': 'http://purl.org/rss/2.0/',
    'triso': 'http://www.trisotech.com/2015/triso/modeling',
    'trisobpmn': 'http://www.trisotech.com/2014/triso/bpmn',
    'trisofeed': 'http://trisotech.com/feed',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

@unique
class Error(Enum):
    NONE = 0
    SCHEMA_INVALID = -101
    SEMANTIC_INVALID = -102
    DEPLOYMENT_INVALID = -103
    IMPL_EXISTING_FILE = -201
    IMPL_DUPE_ID = -202
    DEPLOY_FAILED = -400
    FAILED_AUTH = -401
    DEPLOY_UNSUPPORTED_AUTH_TYPE  = -403
    DEPLOY_UNSUPPORTED_APP  = -405

class KpException(Exception):
    def __init__(self, err):
        self.err = err
        super().__init__()
    def __str__(self):
        return f'{self.err}'

class Configurator():
    CFG_DIR_DEFAULT=Path.home().joinpath('.config')
    CFG_FILE='.kpctl.conf'
    CFG_TEMPLATE='''
    # Configuration for kpctl

    [dev]
    auth_type = Basic
    username = rest-admin
    password = test
    url = http://localhost:8080

    [prod]
    auth_type = openid-connect
    auth_url = https://auth.example.com/auth/realms/realm/protocol/openid-connect/token
    username = admin
    password = secret
    client_id = client1
    client_secret = very-secret-do-not-share
    url = https://prod.example.com
    '''

    def __init__(self, options):
        self.options = options

    def read_config(self, key):
        """Read the local configuration"""

        cfg_file = self.CFG_FILE
        try:
            if self.options.verbose:
                print('CONFIG DIR > ', os.environ['XDG_CONFIG_HOME'])
            cfg_file = Path.joinpath(os.environ['XDG_CONFIG_HOME'], self.CFG_FILE)
        except KeyError:
            if self.options.verbose:
                print('$XDG_CONFIG_HOME not set, fall back to ~/.config/')
            if not(os.path.isdir(self.CFG_DIR_DEFAULT)):
                os.mkdir(self.CFG_DIR_DEFAULT)
            cfg_file = Path.joinpath(self.CFG_DIR_DEFAULT, self.CFG_FILE)

        if cfg_file.is_file():
            if self.options.verbose:
                print('reading configuration [{}]'.format(key))
            config = ConfigParser()
            try:
                config.read(str(cfg_file))

                self.auth_type = config.get(key, 'auth_type')
                self.auth_url = config.get(key, 'auth_url') if 'auth_url' in config[key] else ''
                self.client_id = config.get(key, 'client_id') if 'client_id' in config[key] else ''
                self.client_secret = config.get(key, 'client_secret') if 'client_secret' in config[key] else ''
                self.username = config.get(key, 'username')
                self.password = config.get(key, 'password')
                self.url = config.get(key, 'url')
                if self.options.verbose:
                    print('... authentication type: {} ...'.format(self.auth_type))
                    print('... credentials {}:**** ...'.format(self.username))
            except configparser.NoSectionError as e:
                print("ERROR: No section named '{}' in config file".format(key))
                parser.print_help()
                sys.exit(-1)
            except configparser.NoOptionError as e:
                print("ERROR: reading section named '{}' in config file, detail: {}".format(key, e))
                parser.print_help()
                sys.exit(-1)
        else:
            print('no config file {} found, initialising a default...'.format(self.CFG_FILE))
            file = open(cfg_file, 'w')
            file.write(self.CFG_TEMPLATE)
            file.close()
            os.chmod(cfg_file, 0o600)

            parser.print_help()
            sys.exit(1)

class BpmDocumenter():
    def __init__(self, options):
        self.options = options

    def document(self, input_):
        if self.options.verbose:
            print('generating documentation...')

        if input_.endswith('.bpmn'):
            self.generate_proc_image(input_)
        elif input_.endswith('.form'):
            self.generate_form_image(input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file in files:
                    if file.endswith('.bpmn'):
                        self.generate_proc_image(root+'/'+file)
                    elif file.endswith('.form'):
                        self.generate_form_image(root+'/'+file)

        if self.options.verbose:
            print('...done')

    def generate_form_image(self, form_file):
        if self.options.verbose:
            print('  generating image for ...'+form_file)
            print('  ...not yet implemented...')

    def generate_proc_image(self, bpmn_file):
        if self.options.verbose:
            print('  generating image for ...'+bpmn_file)

        dom = ET.parse(bpmn_file)
        res = requests.get(XSLT_PROC_RENDERER)
        xslt = ET.fromstring(res.content)
        transform = ET.XSLT(xslt)
        diags = dom.findall('//bpmndi:BPMNDiagram', NS)
        for count, diag in enumerate(diags):
            if self.options.verbose:
                print('found diag {}'.format(diag.get('id')))
            newdom = transform(dom, diagramId=ET.XSLT.strparam(diag.get('id')))
            #newdom = transform(dom)
            write_pretty_xml(bpmn_file+'.'+str(count+1)+'.svg', newdom)
            try:
                svg2png(bytestring=ET.tostring(newdom, encoding='unicode'), write_to=bpmn_file+'.png')
            except Exception as e:
                print('  ... unable to create png of the process: {}'.format(e))

            # now generate language variants
            try:
                langs = dom.findall('//i18n:translation[@xml:lang]', NS)
                langs = set(map(lambda x : x.get('{http://www.w3.org/XML/1998/namespace}lang'), langs))
                if (len(langs)>0):
                    if self.options.verbose:
                        print('  detected the following languages: "{}"'.format(langs))
                    for l in langs:
                        if self.options.verbose:
                            print("    generating localised '%s' image ..." % l)
                        newdom = transform(dom, diagramId=ET.XSLT.strparam(diag.get('id')),
                                           lang=ET.XSLT.strparam(l))
                        write_pretty_xml(bpmn_file+'.'+str(count+1)+'.'+l+'.svg', newdom)
                        svg2png(bytestring=ET.tostring(newdom, encoding='unicode'), write_to=bpmn_file+'.'+l+'.png')
                else:
                    if self.options.verbose:
                        print('  ... no translations found to document')
            except KeyError as e:
                if self.options.verbose:
                    print('  ... unable to render translations: {} '.format(e))

class BpmnValidator():
    def __init__(self, options):
        self.options = options

    def validate(self, input_):
        cache()
        if self.options.verbose:
            print('validating...')

        if input_.endswith('.bpmn'):
            self.validate_bpmn(input_)
        else:
            proc_ids = []
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn') and not(file_.endswith('.kp.bpmn')):
                        self.validate_bpmn(root+'/'+file_)
                        dom = ET.parse(root+'/'+file_)
                        for proc in dom.findall('//bpmn:process[@isExecutable="true"]', NS):
                            proc_id = proc.attrib['id']
                        if proc_ids.count(proc_id):
                            print('ERROR: More than one file contains process with id %s' % (proc_id))
                            raise KpException(Error.IMPL_DUPE_ID)
                else:
                    proc_ids.append(proc_id)

        if self.options.verbose:
            print('...done')

    def validate_bpmn(self, bpmn_file):
        if self.options.verbose:
            print('  validating ...'+bpmn_file)
        colorama.init()

        try:
            issues = self.validate_xsd(bpmn_file)
            if issues[0:5] == 'ERROR':
                print(issues)

            issues += str(transform(XSLT_VALIDATOR, bpmn_file))
            issues += str(transform(XSLT_EXT_VALIDATOR, bpmn_file))

            issueArr = issues.split('\n')
            errs = list(filter(lambda issue: issue[0:5] == 'ERROR', issueArr))
            print('\n'.join(errs).replace('ERROR',Fore.RED + 'ERROR' + Style.RESET_ALL))
            warns = list(filter(lambda issue: issue[1:5] == 'WARN', issueArr))
            print('\n'.join(warns).replace('WARN',Fore.YELLOW + 'WARN' + Style.RESET_ALL))
            infos = list(filter(lambda issue: issue[1:5] == 'INFO', issueArr))
            debugs = list(filter(lambda issue: issue[0:5] == 'DEBUG', issueArr))

            if self.options.verbose:
                print('\n'.join(infos).replace('INFO',Fore.GREEN+ 'INFO' + Style.RESET_ALL))
            if self.options.debug:
                print('\n'.join(debugs).replace('DEBUG',Fore.GREEN+ 'DEBUG' + Style.RESET_ALL))
            print('\n  %s %s schema valid and has %d errors, %d warnings and %d messages.'
                % (bpmn_file, ('is' if 'is schema valid' in issueArr[0] else 'is not'),
                    len(errs), len(warns), len(infos)))
            if len(errs) > 0:
                raise KpException(Error.DEPLOYMENT_INVALID)
        except ET.XMLSyntaxError as e:
            issue = "ERROR: file '%s' is not well-formed XML, individual issues follow:\n" % (bpmn_file)
            for err in e.error_log:  # pylint: disable=no-member
                issue += "ERROR: Line %s: %s\n" % (err.line, err.message)
            print(issue)
            raise KpException(Error.SCHEMA_INVALID)

    def validate_xsd(self, xml_path: str) -> bool:
        xmlschema_doc = ET.parse(BPMN_XSD_ROOT_PATH)
        xmlschema = ET.XMLSchema(xmlschema_doc)
        try:
            xml_doc = ET.parse(xml_path)
            xmlschema.assertValid(xml_doc)
            return " INFO: file '%s' is schema valid\n" % (xml_path)
        except ET.XMLSyntaxError as e:
            issue = "ERROR: file '%s' is not well-formed XML, individual issues follow:\n" % (xml_path)
            for err in e.error_log:  # pylint: disable=no-member
                issue += "ERROR: Line %s: %s\n" % (err.line, err.message)
            return issue
        except ET.DocumentInvalid as e:
            issue = "ERROR: file '%s' is not schema valid, individual issues follow:\n" % (xml_path)
            for err in e.error_log:  # pylint: disable=no-member
                issue += "ERROR: Line %s: %s\n" % (err.line, err.message)
            return issue

class BpmnEditor():
    def __init__(self, options):
        self.options = options

    def describe(self, id_, input_):
        if input_.endswith('.bpmn'):
            self.describe_from_file(id_, input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.describe_from_file(id_, root+'/'+file_)

    def describe_from_file(self, id_, bpmn_file):
        if self.options.verbose:
            print('describing {} within {} ...'.format(id_, bpmn_file))
        colorama.init()

        dom = ET.parse(bpmn_file)
        objs = dom.findall("//*[@id='{}']".format(id_), NS)
        for obj in objs:
            ltag = local_tag(obj)
            print('  {}{}{}:{} {}'.format(Style.BRIGHT, Fore.GREEN,
                                          ltag, Style.RESET_ALL, obj.attrib['id']))
            for key in obj.keys():
                 if key != 'id':
                     print('    {}{}:{} {}'.format(Fore.GREEN, key, Style.RESET_ALL,
                                                   obj.attrib[key].replace('\n', ' ')))

            if (ltag in ['sendTask', 'serviceTask', 'businessRuleTask']):
                for platform in ['activiti','camunda','flowable','kp']:
                    exts = obj.findall(".//{}:field".format(platform), NS)
                    if (len(exts)>0):
                        print('    {}{}{} extension:{}'.format(Style.BRIGHT, Fore.CYAN,
                                                           platform, Style.RESET_ALL))
                    for ext in exts:
                        value = ext.attrib['expression'] if 'expression' in ext.keys() else ext.attrib['stringValue']
                        print('      {}{}:{} {}'.format(Fore.CYAN, ext.attrib['name'],
                                                        Style.RESET_ALL, value))
                    refType = obj.find(".//{}:decisionReferenceType".format(platform), NS)
                    if refType != None:
                        print('      {}decisionReferenceType:{} {}'.format(Fore.CYAN,
                                                        Style.RESET_ALL, refType.text))

            elif (ltag == 'userTask'):
                po = obj.find('.//bpmn:formalExpression', NS)
                print('    {}potentialOwner:{} {}'.format(Fore.GREEN,
                                                          Style.RESET_ALL,
                                                          'n/a' if po is None else po.text))

            di = dom.find("//*[@bpmnElement='{}']".format(id_), NS)
            if (di is None):
                print('  no diagram interchange information is available')
            else:
                print('  {}{}{}:{} {}'.format(Style.BRIGHT, Fore.MAGENTA,
                                              local_tag(di), Style.RESET_ALL, di.get('id', 'n/a')))
                for key in di.keys():
                     if key != 'id':
                         print('    {}{}:{} {}'.format(Fore.MAGENTA, key,
                                                       Style.RESET_ALL,
                                                       di.attrib[key].replace('\n', ' ')))
                di_bounds = di.find('dc:Bounds', NS)
                if di_bounds != None:
                    print('    {}{}:{} position {},{} size {},{}'.format(
                               Fore.MAGENTA, 'bounds', Style.RESET_ALL,
                               di_bounds.get('x','n/a'), di_bounds.get('y','n/a'),
                               di_bounds.get('width','n/a'), di_bounds.get('height','n/a')))
                else:
                    print('    no bounds information')
                di_label = di.find('bpmndi:BPMNLabel', NS)
                if di_label != None:
                    print('    {}{}:{} {}'.format(Fore.MAGENTA, local_tag(di_label),
                                                  Style.RESET_ALL, di.get('id','n/a')))
                    for key in di_label.keys():
                        if key != 'id':
                            print('      {}{}:{} {}'.format(Fore.MAGENTA, key,
                                                            Style.RESET_ALL,
                                                            di_label.attrib[key]))
                    di_label_bounds = di_label.find('dc:Bounds', NS)
                    if di_label_bounds != None:
                        print('      {}{}:{} position {},{} size {},{}'.format(
                                   Fore.MAGENTA, 'bounds', Style.RESET_ALL,
                                   di_label_bounds.get('x', 'n/a'),
                                   di_label_bounds.get('y', 'n/a'),
                                   di_label_bounds.get('width', 'n/a'),
                                   di_label_bounds.get('height', 'n/a')))
                    else:
                        print('    no label bounds information')
                else:
                    print('    no label information')

    def get(self, type_, input_):
        if input_.endswith('.bpmn'):
            self.get_from_file(type_, input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.get_from_file(type_, root+'/'+file_)

    def get_from_file(self, type_, bpmn_file):
        if self.options.verbose:
            print('finding {} within {} ...'.format(type_, bpmn_file))
        colorama.init()

        dom = ET.parse(bpmn_file)
        objs = dom.findall('//{}'.format((type_, 'bpmn:'+type_) [type_.find(':')==-1]), NS)
        for obj in objs:
            print('  {}{}{}: {}'.format(Fore.GREEN, obj.attrib['id'],
                                        Style.RESET_ALL,
                                        'n/a' if obj.get('name') == None else obj.get('name')))

    def set_(self, id_, target, value, input_):
        if input_.endswith('.bpmn'):
            self.set_in_file(id_, target, value, input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.set_in_file(id_, target, value, root+'/'+file_)

    def set_in_file(self, id_, target, value, bpmn_file):
        if self.options.verbose:
            print('setting {} of {} to {} ...'.format(target, id_, value))

        dom = ET.parse(bpmn_file)
        obj = dom.find("//*[@id='{}']".format(id_), NS)

        if (target.find(':') > -1):
            target = '{'+NS[target[0:target.find(':')]]+'}'+target[target.find(':')+1:]
        if (obj == None):
            if self.options.verbose:
                print('  object not found')
        else:
            obj.set(target, value)
            self.write_kp_bpmn(bpmn_file, dom)

    def set_ext(self, id_, target, value, input_):
        if input_.endswith('.bpmn'):
            self.set_ext_in_file(id_, target, value, input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.set_ext_in_file(id_, target, value, root+'/'+file_)

    def set_ext_in_file(self, id_, target, value, bpmn_file):
        if self.options.verbose:
            print('set extension {} of {} to {} ...'.format(target, id_, value))

        dom = ET.parse(bpmn_file)
        obj = dom.find("//*[@id='{}']/bpmn:extensionElements/*[@name='{}']".format(id_, target), NS)
        if (obj is None):
            exts = dom.find("//*[@id='{}']/bpmn:extensionElements".format(id_), NS)
            ext = ET.SubElement(exts, ('{%s}field' % NS['kp']))
            ext.set('name', target)
            if value.find('${')==-1:
                print('  adding new extension string {}'.format(target))
                ext.set('stringValue', value)
            else:
                print('  adding new extension expression {}'.format(target))
                ext.set('expression', value)
            exts.append(ext)
        else:
            if value.find('${')==-1:
                print('  updating existing extension string {}'.format(target))
                obj.set('stringValue', value)
            else:
                print('  updating existing extension expression {}'.format(target))
                obj.set('expression', value)
        self.write_kp_bpmn(bpmn_file, dom)

    def set_res(self, id_, value, input_):
        if input_.endswith('.bpmn'):
            self.set_res_in_file(id_, value, input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.set_res_in_file(id_, value, root+'/'+file_)

    def set_res_in_file(self, id_, value, bpmn_file):
        if self.options.verbose:
            print('set resource of {} to {} ...'.format(id_, value))

        dom = ET.parse(bpmn_file)
        obj = dom.find("//*[@id='{}']/bpmn:potentialOwner".format(id_), NS)
        if (obj is None):
            task = dom.find("//*[@id='{}']".format(id_), NS)
            po = ET.SubElement(task, ('{%s}potentialOwner' % NS['bpmn']))
            resExpr = ET.SubElement(po, ('{%s}resourceAssignmentExpression' % NS['bpmn']))
            expr = ET.SubElement(resExpr, ('{%s}formalExpression' % NS['bpmn']))
            expr.text = value
            resExpr.append(expr)
            po.append(resExpr)
            task.append(po)
        else:
            dom.find("//*[@id='{}']/bpmn:potentialOwner//bpmn:formalExpression".format(id_), NS).text = value
        self.write_kp_bpmn(bpmn_file, dom)

    def write_kp_bpmn(self, path, dom):
        dom.getroot().set('exporter', APP_NAME)
        dom.getroot().set('exporterVersion', APP_VSN)
        write_pretty_xml(path, dom)

class BpmDeployer():

    DEPLOYMENT_API = '/flowable-rest/app-api/app-repository/deployments'

    def __init__(self, options, configurator, validator):
        self.options = options
        self.configurator = configurator
        self.validator = validator

    def deploy(self, app, target):
        if self.options.verbose:
            print('deploying {} to {} ...'.format(app, target))

        if not app.endswith('bar') and not app.endswith('zip'):
            if self.options.verbose:
                print('... cannot deploy \''+app+'\', must be .bar or .zip')
            raise KpException(Error.DEPLOY_UNSUPPORTED_APP)

        self.configurator.read_config(target)
        if self.configurator.auth_type == 'Basic':
            r = requests.post(self.get_deployment_api(self.configurator.url), data={'file':app},
                files={'file': open(app, 'rb')},
                auth = HTTPBasicAuth(self.configurator.username, self.configurator.password))
            if r.status_code <= 400:
                if self.options.verbose:
                    print('...done, status: '+str(r.status_code))
            else:
                if self.options.verbose:
                    print('...error: '+str(r.status_code))
                raise KpException(Error.DEPLOY_FAILED)
        else:
            if self.options.verbose:
                print('... unsupported authentication type {}'.format(self.configurator.auth_type))
            raise KpException(Error.DEPLOY_UNSUPPORTED_AUTH_TYPE)

    def generate_app(self, root):
        appPath = '%s/%s.app' % (root, root)
        if exists(appPath) and not(args.force):
            if self.options.verbose:
                print("  ... app '%s' already exists, --force to overwrite" % appPath)
        else:
            count = 0
            for filename in glob.glob(root+"/*.app"):
                if self.options.verbose:
                    print("  ... found '%s', not generating another app descriptor" % filename)
                count += 1

            if count == 0:
                if self.options.verbose:
                    print('  generating app at %s ...' % root)
                file = open(appPath, 'w')
                key = root[0:1].upper() + root[1:]
                file.write(TEMPLATE_APP_DESCRIPTOR % (key, key))
                file.close()

    def generate_forms(self, bpmn_file):
        if self.options.verbose:
            print('  generating forms for ...'+bpmn_file)

        dom = ET.parse(bpmn_file)
        for startEvent in dom.findall('//bpmn:startEvent', NS):
            self.generate_form(bpmn_file, dom, startEvent)
        for userTask in dom.findall('//bpmn:userTask', NS):
            self.generate_form(bpmn_file, dom, userTask)

    def generate_form(self, bpmn_file, dom, bpmn_obj):
        name = bpmn_obj.get('name')
        formKey = bpmn_obj.get('{http://knowprocess.com/bpmn}formKey')
        if formKey == None:
            formKey = bpmn_obj.get('{http://flowable.org/bpmn}formKey')
        formPath = '%s/%s.form' % (bpmn_file[:bpmn_file.rfind('/')], formKey)

        if formKey == None:
            if self.options.verbose:
                print("  ... found %s '%s', but it has no formKey"
                    % (local_tag(bpmn_obj), name))
        elif exists(formPath) and not(args.force):
            if self.options.verbose:
                print("  ... found %s '%s', but form already exists with key '%s' --force to overwrite"
                    % (local_tag(bpmn_obj), name, formKey))
        else:
            print("  ... generating stub form '%s'" % formKey)
            fields = ''
            data_inputs = dom.findall('//bpmn:process/bpmn:ioSpecification/bpmn:dataInput', NS) if (local_tag(bpmn_obj) == 'startEvent') else dom.findall('//*[@id="{}"]//bpmn:dataInput'.format(bpmn_obj.get('id')), NS)
            for count, data_input in enumerate(data_inputs):
                fields += TEMPLATE_FORM_FIELD % (camel_case(data_input.get('name')),
                                                data_input.get('name'))
                if (count+1 < len(data_inputs)):
                    fields += ','
            file = open(formPath, 'w')
            file.write(TEMPLATE_FORM % (formKey, formKey if name == None else name, fields))
            file.close()

    def generate_proc_executable(self, bpmn_file):
        if self.options.verbose:
            print('  generating executable process for %s ...' % bpmn_file)

        fileStart = int(bpmn_file.rfind('/'))+1
        implPath = '%s/%s.kp.bpmn' % (bpmn_file[:fileStart], bpmn_file[fileStart:bpmn_file.rfind('.')]) if fileStart > 0 else ('%s.kp.bpmn' % bpmn_file[:bpmn_file.rfind('.')])
        if exists(implPath):
            if self.options.verbose:
                print("  ... overwriting executable process '%s' ..." % (implPath))

        dom = ET.parse(bpmn_file)
        res = requests.get(XSLT_PROC_ENHANCER)
        xslt = ET.fromstring(res.content)
        transform = ET.XSLT(xslt)
        write_pretty_xml(implPath, transform(dom, unsupportedTasksToUserTask=ET.XSLT.strparam('false')))

    def get_deployment_api(self, target):
        if self.options.verbose:
            print('deploying to {}{}...'.format(target, self.DEPLOYMENT_API))

        return target+self.DEPLOYMENT_API

    def implement(self, input_):
        if self.options.verbose:
            print('generating implementation hints...')

        if input_.endswith('.bpmn'):
            self.generate_forms(input_)
            if not input_.endswith('.kp.bpmn'):
                self.generate_proc_executable(input_)
        else:
            for root, dirs, files in os.walk(input_):
                self.generate_app(root)
                for file_ in files:
                    if file_.endswith('.bpmn'):
                        self.generate_forms(root+'/'+file_)
                        if not file_.endswith('.kp.bpmn'):
                            self.generate_proc_executable(root+'/'+file_)

        if self.options.verbose:
            print('...done')

    def is_executable(self, file_name):
        if (file_name.endswith('kp.bpmn')):
            dom = ET.parse(file_name)
            return dom.findall('//bpmn:process[@isExecutable="true"]', NS)
        else:
            exts_inc = tuple(['app', 'form', 'md', 'txt'])
            return file_name.endswith(exts_inc)

    # Zip the files from given directory that matches the filter
    def zipFilesInDir(self, dirName, zipFileName, filter):
        # create a ZipFile object
        with ZipFile(zipFileName, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(dirName):
                for filename in filenames:
                    if filter(filename):
                        # create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        if self.options.verbose:
                            print('  adding: {}'.format(filePath))
                        zipObj.write(filePath, basename(filePath))

    def package(self, dir_name, file_name):
        if file_name == None:
            file_name = dir_name

        self.validator.validate(dir_name)
        self.implement(dir_name)

        if self.options.verbose:
            print('packaging {}.zip from {} ...'.format(file_name, dir_name))
        self.zipFilesInDir(dir_name, file_name+'.zip', lambda name : self.is_executable(os.path.join(dir_name, name)))

        if self.options.verbose:
            print('...done')

class Curl():

    def __init__(self, options, configurator):
        self.options = options
        self.configurator = configurator

    def get_token(self, target):
        self.configurator.read_config(target)

        if self.options.verbose:
            print('attempt to login to {} ...'.format(self.configurator.auth_url))

        try:
            oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.configurator.client_id))
            token = oauth.fetch_token(token_url=self.configurator.auth_url, client_id=self.configurator.client_id,
                                      username=self.configurator.username, password=self.configurator.password)
            if self.options.verbose:
                print('... login succeeded')
            self.configurator.auth = 'Bearer '+token['access_token']
            return self.configurator.auth
        except Exception as e:
            print('{} Unable to login'.format(e))
            raise KpException(Error.FAILED_AUTH)

    def make_request(self, target, req_options):
        if self.options.verbose:
            print('making request to {} ...'.format(req_options.url))

        self.configurator.read_config(target)
        if self.configurator.auth_type == 'Basic':
            bytes_ = (self.configurator.username+':'+self.configurator.password).encode('utf-8')
            encodedBytes = str(base64.b64encode(bytes_), 'utf-8')
            self.configurator.auth = 'Basic {}'.format(encodedBytes)
        elif self.configurator.auth_type == 'openid-connect':
            self.get_token(target)
        else:
            if self.options.verbose:
                print('... unsupported authentication type {}'.format(self.configurator.auth_type))
            raise KpException(Error.DEPLOY_UNSUPPORTED_AUTH_TYPE)

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": self.configurator.auth,
            "X-RunAs": self.configurator.username
        }
        if self.options.verbose:
            print('... headers: {} ...'.format(headers))

        if self.options.verbose:
            print('connecting to {}'.format(req_options.url))

        if req_options.data:
            if self.options.verbose:
                print('payload is: {}'.format(req_options.data))
            if req.data.find('=') != -1:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                if self.options.verbose:
                    print('content type: {}'.format(headers['Content-Type']))
            data = req_options.data.encode('utf-8')
            req = urllib.request.Request(req_options.url, data, headers = headers)
        else:
            req = urllib.request.Request(req_options.url, headers = headers)

        if req_options.verb:
            if self.options.verbose:
                print('HTTP method: '+req_options.verb)
            req.get_method = lambda: req_options.verb
        try:
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            if self.options.verbose:
                print('SUCCESS')
            print(respData.decode('UTF-8'))
        except urllib.error.HTTPError as e:
            if self.options.verbose:
                print('ERROR: {}: {}'.format(e.code, e.reason))

def cache():
    if args.verbose:
        print('caching external resources...')

    if not(exists(CACHE_DIR)):
        mkdir(CACHE_DIR, 0o755)
        if not(exists(CACHE_DIR + '/xsd')):
            mkdir(CACHE_DIR + '/xsd', 0o755)

    cache_file(XSD_BPMN, CACHE_DIR + '/xsd/BPMN20.xsd')
    cache_file(XSD_BPMNDI, CACHE_DIR + '/xsd/BPMNDI.xsd')
    cache_file(XSD_DC, CACHE_DIR + '/xsd/DC.xsd')
    cache_file(XSD_DI, CACHE_DIR + '/xsd/DI.xsd')
    cache_file(XSD_SEMANTIC, CACHE_DIR + '/xsd/Semantic.xsd')

    if args.verbose:
      print('... done.')

def cache_file(url, file_path):
    if not(exists(file_path)):
        if args.verbose:
            print('...%s...' % (file_path))

        file = open(file_path, 'wb')
        file.write(requests.get(url).content)
        file.close()

def camel_case(s):
    return s[0:1].lower() + s[1:].replace(' ','')

def local_tag(obj):
    return (obj.tag[obj.tag.find('}')+1:], obj.tag) [obj.tag.find('}')==-1]

def help(parser):
    print('{} {}'.format(__name__, kpctl.__version__))
    parser.print_help()

def transform(xsl_file, xml_file):
    dom = ET.parse(xml_file)
    res = requests.get(xsl_file)
    xslt = ET.fromstring(res.content)
    try:
      transform = ET.XSLT(xslt)
    except Exception as e:
      print(e)
    if args.debug:
      return transform(dom, verbosity="0")
    else:
      # collect all (v=1) and let decide calling func decide what to report
      return transform(dom, verbosity="1")

def write_pretty_xml(path, dom):
    # despite many examples of parsing pretty_print=True to ET.tostring
    # my experience is that it does not work, so reluctantly duplicating parsing
    reparsed = parseString(ET.tostring(dom, encoding="utf-8"))
    pretty_print = '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()])
    with open(path, 'w') as f:
        f.write(pretty_print)

def main():
    '''Main entry point to kpctl'''

    parser = argparse.ArgumentParser(prog="kpctl", add_help=False)
    parser.add_argument("-f", "--force", help="overwrite existing files",
        action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
        action="store_true")
    parser.add_argument("-X", "--debug", help="extra verbose output for debugging",
        action="store_true")
    subparser = parser.add_subparsers(dest="cmd")

    cache_parser = subparser.add_parser('cache', help='cache resources used elsewhere')

    validate_parser = subparser.add_parser('validate', help='validate (esp. bpmn)')
    validate_parser.add_argument("input", help="source file or folder")

    generate_parser = subparser.add_parser('document', help='generate documentation')
    generate_parser.add_argument("input", help="source file or folder")

    impl_parser = subparser.add_parser('implement', help='generate implementation tips')
    impl_parser.add_argument("input", help="source file or folder")

    get_parser = subparser.add_parser('get', help='get a list of objects with type')
    get_parser.add_argument("type", help="object type to get")
    get_parser.add_argument("input", help="source file or folder")

    describe_parser = subparser.add_parser('describe', help='describe the specified object')
    describe_parser.add_argument("id", help="object to describe")
    describe_parser.add_argument("input", help="source file or folder")

    set_parser = subparser.add_parser('set', help='set a new value of the specified object')
    set_parser.add_argument("id", help="object to update")
    set_parser.add_argument("target", help="the part of the object being targetted")
    set_parser.add_argument("value", help="value to set")
    set_parser.add_argument("input", help="source file or folder")

    set_ext_parser = subparser.add_parser('setextension', help='set a new value of the specified object extension')
    set_ext_parser.add_argument("id", help="object to update")
    set_ext_parser.add_argument("target", help="the extension being targetted")
    set_ext_parser.add_argument("value", help="value to set")
    set_ext_parser.add_argument("input", help="source file or folder")

    set_res_parser = subparser.add_parser('setresource', help='set a resource for a task')
    set_res_parser.add_argument("id", help="task to update")
    set_res_parser.add_argument("value", help="value to set")
    set_res_parser.add_argument("input", help="source file or folder")

    package_parser = subparser.add_parser('package', help='create deployable file from source')
    package_parser = subparser.add_parser('package', help='create deployable file from source')
    package_parser.add_argument("input", help="directory containing source files")
    package_parser.add_argument("-o", "--output", help="file name for archive to create",
            default=None)

    deploy_parser = subparser.add_parser('deploy', help='deploy a deployable file to a server')
    deploy_parser.add_argument("app", help="name of application archive to deploy")
    deploy_parser.add_argument("target", help="logical name for target server (section heading of config file)")
    deploy_parser.add_argument("-u", "--user", help="user to perform deployment")
    deploy_parser.add_argument("-p", "--password", action="store_true",
            help="prompt for password to perform deployment")

    curl_parser = subparser.add_parser('curl', help='query / update server endpoints')
    curl_parser.add_argument("target", help="logical name for target server (section heading of config file)")
    curl_parser.add_argument("url", help="api url to call")
    curl_parser.add_argument("-d", "--data", help="payload, if expected by server")
    curl_parser.add_argument("-X", "--verb", help="specify HTTP verb explicitly (GET and POST are implicit)")

    subparser.add_parser('help', help='show this help')

    # custom help message
    parser._positionals.title = "commands"

    args = parser.parse_args()
    configurator = Configurator(args)
    documenter = BpmDocumenter(args)
    validator = BpmnValidator(args)
    editor = BpmnEditor(args)
    deployer = BpmDeployer(args, configurator, validator)
    curl = Curl(args, configurator)

    try:
        if args.cmd == 'cache':
            cache()
        elif args.cmd == 'validate':
            validator.validate(args.input)
        elif args.cmd == 'describe':
            editor.describe(args.id, args.input)
        elif args.cmd == 'document':
            documenter.document(args.input)
        elif args.cmd == 'get':
            editor.get(args.type, args.input)
        elif args.cmd == 'set':
            editor.set_(args.id, args.target, args.value, args.input)
        elif args.cmd == 'setextension':
            editor.set_ext(args.id, args.target, args.value, args.input)
        elif args.cmd == 'setresource':
            editor.set_res(args.id, args.value, args.input)
        elif args.cmd == 'implement':
            deployer.implement(args.input)
        elif args.cmd == 'package':
            deployer.package(args.input, args.output)
        elif args.cmd == 'deploy':
            if (args.password):
                args.password = getpass()
            deployer.deploy(args.app, args.target)
        elif args.cmd == 'curl':
            curl.make_request(args.target, args)
        else:
            help(parser)
        sys.exit(0)
    except KpException as e:
        sys.exit(e.err.value)

