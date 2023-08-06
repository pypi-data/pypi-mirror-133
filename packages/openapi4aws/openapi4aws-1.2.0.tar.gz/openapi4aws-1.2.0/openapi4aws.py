"""openapi4aws - utility to enrich an openapi specification with information
specific for the AWS API Gateway.
It allows defining route integrations and authorizers to do automatic
(re-)imports in API Gateway.

Author:  Luis M. Pena <lu@coderazzi.net>
Site:    https://coderazzi.net/python/openapi4ws
"""

import glob
import os.path
import re
import sys
from dataclasses import dataclass

import yaml


__version__ = '1.2.0'

__all__ = ['openapi4aws', 'augment_content', 'Configuration', 'ConfigurationError']

__copyright__ = """
Copyright (c) Luis M. Pena <lu@coderazzi.net>  All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


class Configuration:
    """Class to parse the arguments and define the configuration"""

    AUTHORIZER_AUTHORIZATION_TYPE = 'authorization-type'
    AUTHORIZER_TYPE = 'authorizer-type'
    DEFAULT_AUTHORIZER = {AUTHORIZER_TYPE: "oauth2",
                          AUTHORIZER_AUTHORIZATION_TYPE: 'jwt'}
    SIMPLE_AUTHORIZER_FIELDS = {AUTHORIZER_AUTHORIZATION_TYPE, AUTHORIZER_TYPE,
                                'identity-source', 'issuer'}
    AUTHORIZER_FIELDS = SIMPLE_AUTHORIZER_FIELDS.union({'audience'})
    CONFIGURATION_ARGUMENT = "configuration"
    AUTHORIZER_ARGUMENT = "authorizer."
    AUTHORIZER_DEFINITION = "name"
    ARGUMENTS_PRIORITY = [AUTHORIZER_ARGUMENT + AUTHORIZER_DEFINITION, CONFIGURATION_ARGUMENT]

    @staticmethod
    def from_filename(filename):
        return Configuration(['%s=%s' % (Configuration.CONFIGURATION_ARGUMENT, filename)])

    def __init__(self, argv):
        self.output_folder = None
        self.authorizers = {}
        self.filenames = set()
        self.globs = set()
        self.tags = {}
        self.paths = {}
        self.argument_handlers = {
            self.AUTHORIZER_ARGUMENT: self._handle_authorizer,
            self.CONFIGURATION_ARGUMENT: self._handle_configuration,
            'tag.': self._handle_tag,
            'path.': self._handle_path,
            'filename': self._handle_filename,
            'glob': self._handle_glob,
            'output-folder': self._handle_output
        }
        self.arg_pattern = re.compile("^(--)?(%s)([^=]*)=(.+)$" %
                                      '|'.join(self.argument_handlers.keys()))
        self._handle_arguments(argv, False)
        self._check_authorizer_definitions()

    def get_input(self):
        """Returns a set of all specified inputs"""
        ret = set(self.filenames)
        for g in self.globs:
            ret = ret.union(glob.iglob(g))
        return ret

    def get_output(self):
        """Returns the specified output folder"""
        return self.output_folder

    def get_authorizers(self):
        """Returns authorizers as tuples (name, audience, authorization_type,
        authorizer_type, identity, issuer)"""
        return [(k, *[v[field] for field in sorted(self.AUTHORIZER_FIELDS)])
                for k, v in self.authorizers.items() if k]

    def get_integration(self, path, tags):
        """Returns the most suitable integration for the given path,
        as tuple(authorizer, scopes, uri)"""
        try:
            ret = self.paths[path]
        except KeyError:
            ret = None
            for tag in tags:
                try:
                    ret = self.tags[tag.lower()]
                    break
                except KeyError:
                    pass
        if ret:
            return ret.authorizer, ret.scopes, ret.uri(path)

    def _handle_arguments(self, argv, strict):
        """Parses the given arguments. If strict is True,
        arguments cannot be preceded with dashes"""
        for argument, area, name, value in self._sort_arguments(argv, strict):
            try:
                self.argument_handlers[area](name, value)
            except ConfigurationError as ae:
                raise ConfigurationError(argument + ' : ' + ae.args[1])

    def _sort_arguments(self, argv, strict):
        """Return the arguments sorted, as (arg, area, name, value),
        raising an exception if arguments are incorrect"""

        def get_priority(argument):
            try:
                # if argument is defined in self.ARGUMENTS_PRIORITY, return a negative value
                return self.ARGUMENTS_PRIORITY.index(argument) - len(self.ARGUMENTS_PRIORITY)
            except ValueError:
                # respect input order, returning the current position in input order
                return len(ret)

        ret = []
        using_dashes = False if strict else None
        for arg in argv:
            m = self.arg_pattern.match(arg)
            if m:
                opt, area = m.group(1) is not None, m.group(2)
                name, value = m.group(3).strip(), m.group(4).strip()
                if using_dashes is None or using_dashes == opt:
                    using_dashes = opt
                    # if area ends wih '.', name cannot be empty
                    if value and (area.endswith('.') != (name == '')):
                        ret.append((get_priority(area + name), arg, area, name, value))
                        continue
            raise ConfigurationError(ConfigurationError.UNEXPECTED_ARGUMENT + ' : ' + arg)
        return [[y for y in x[1:]] for x in sorted(ret)]

    def _check_authorizer_definitions(self):
        """Checks that all integrations are fully defined"""
        for name, auth in self.authorizers.items():
            if name:
                for field in self.AUTHORIZER_FIELDS:
                    if field not in auth:
                        missing = self.AUTHORIZER_ARGUMENT + field
                        raise ConfigurationError(f'Missing {missing} or {missing}.{name}')

    @staticmethod
    def _convert_to_non_empty_list(arg):
        """Splits a string with commas separator into its not empty parts.
           There must be at least one part, or an exception is raised"""
        ret = [y for y in [x.strip() for x in arg.split(',')] if y]
        if not ret:
            raise ConfigurationError('Invalid value: ' + arg)
        return ret

    def _handle_configuration(self, _, filename):
        """Handles an argument configuration=value,
        by reading the arguments specified in the given filename"""
        with open(filename) as f:
            argv = [y for y in [x.strip() for x in f.readlines()] if y and not y.startswith('#')]
            self._handle_arguments(argv, True)

    def _handle_glob(self, _, value):
        """Handles an argument glob=value"""
        self.globs.add(value)

    def _handle_filename(self, _, value):
        """Handles an argument filename=value"""
        self.filenames.add(value)

    def _handle_output(self, _, value):
        """Handles an argument output-folder=value"""
        self.output_folder = value

    def _handle_path(self, definition, value):
        """Handles an argument path.definition=value,
        where value is uri[,authorizer,scopes]"""
        uri, *plus = self._convert_to_non_empty_list(value)
        self.paths['/' + definition.replace('.', '/')] = self._new_integration(plus, lambda _: uri)

    def _handle_tag(self, definition, value):
        """Handles an argument tag.definition=value,
        where value is uri[,authorizer,scopes]"""
        uri, *other = self._convert_to_non_empty_list(value)
        if uri.endswith('/'):
            uri = uri[:-1]
        self.tags[definition.lower()] = self._new_integration(other, lambda path: uri + path)

    def _new_integration(self, auth_items, uri_function):
        """Creates an Integration
           :param auth_items: None or authorizer, [scopes]
           :param uri_function: used to create the final uri for a given path
        """
        if auth_items:
            authorizer, *scopes = auth_items
            if authorizer not in self.authorizers:
                raise ConfigurationError(authorizer + ' is not a provided authorizer name')
        else:
            authorizer, scopes = None, []
        return Integration(uri=uri_function, authorizer=authorizer, scopes=scopes)

    def _handle_authorizer(self, definition, value):
        """Handles an argument authorizer.definition=value"""
        if self.AUTHORIZER_DEFINITION == definition:
            # main authorizer definitions, defines the name of the authorizers
            try:
                default_authorizer = self.authorizers['']
            except KeyError:
                # define the default authorizer as without name, as that matches then the
                # definitions without authorizer name such as authorizer.issuer = value,
                # as opposed to authorizer.issuer.name = value
                default_authorizer = Authorizer(self.DEFAULT_AUTHORIZER)
                self.authorizers[''] = default_authorizer
            for x in self._convert_to_non_empty_list(value):
                if x not in self.authorizers:
                    self.authorizers[x] = Authorizer(default_authorizer)
        else:
            # definition can include the authorizer: 'issuer.authorizer_name'
            last = definition.rfind('.')
            if last == -1:
                name = ''
            else:
                name = definition[last + 1:].strip()
                definition = definition[:last].strip()
            if definition not in self.AUTHORIZER_FIELDS or name not in self.authorizers:
                raise ConfigurationError(ConfigurationError.UNEXPECTED_ARGUMENT)
            self.authorizers[name][definition] = value


class ConfigurationError(Exception):
    UNEXPECTED_ARGUMENT = 'unexpected argument'

    def __init__(self, msg):
        super().__init__(self, msg)


class Authorizer(dict):
    """Implementation of authorizer as a dictionary where the keys
    can be defined in a delegated dictionary"""

    def __init__(self, delegate):
        super().__init__()
        self.base = delegate

    def __missing__(self, key):
        return self.base[key] if self.base else None

    def __contains__(self, item):
        return super().__contains__(item) or (self.base and item in self.base)


@dataclass
class Integration:
    uri: str
    scopes: str
    authorizer: str


def augment_content(yaml_content, authorizers, integration_getter):
    """Augments the yaml content with the given authorizers and the
       integration provider: path, tags
       :returns True if the content is modified
       """

    def _get_or_create_yaml_field(yaml_spec, field, default_value):
        """Returns the given field in the yaml specification.
        If not found, it creates it with the default value"""
        ret = yaml_spec.get(field)
        if ret is None:
            yaml_spec[field] = ret = default_value
        return ret

    def _define_authorizer(yaml_spec, name, audience, authorization_type,
                           authorizer_type, identity, issuer):
        components = _get_or_create_yaml_field(yaml_spec, 'components', {})
        schemas = _get_or_create_yaml_field(components, 'securitySchemes', {})
        schemas[name] = {
            "type": authorization_type,
            "flows": {},
            "x-amazon-apigateway-authorizer": {
                "identitySource": identity,
                "type": authorizer_type,
                "jwtConfiguration": {
                    "audience": audience.split(','),
                    "issuer": issuer
                }
            }
        }

    def _define_integration(http_method, yaml_spec, authorizer_name, scopes, uri):
        yaml_spec['x-amazon-apigateway-integration'] = {
            'payloadFormatVersion': '1.0',
            'type': 'http_proxy',
            'connectionType': 'INTERNET',
            'httpMethod': http_method.upper(),
            'uri': uri
        }
        if authorizer_name:
            use = _get_or_create_yaml_field(yaml_spec, 'security', [])
            use.clear()
            use.append({authorizer_name: scopes})

    modified = len(authorizers) > 0
    for authorizer in authorizers:
        _define_authorizer(yaml_content, *authorizer)
    for path, path_spec in yaml_content.get('paths', {}).items():
        for method, method_spec in path_spec.items():
            integration = integration_getter(path, method_spec.get('tags', []))
            if integration:
                _define_integration(method, method_spec, *integration)
                modified = True
    return modified


def openapi4aws(configuration):
    def _get_input():
        """Returns tuples (filename, yaml content)"""
        for each in configuration.get_input():
            try:
                with open(each) as fo:
                    yield each, yaml.load(fo, Loader=yaml.FullLoader)
            except IOError as ioex:
                print(f"Error accessing '{each}' : {ioex.strerror}", file=sys.stderr)
            except yaml.MarkedYAMLError as eyx:
                print(f"Invalid yaml file '{each}' : {eyx.problem}", file=sys.stderr)

    for filename, content in _get_input():
        """Returns tuples (name, authorization_type, identity, issuer,
        authorizer_type, audience)"""

        modified = augment_content(content, configuration.get_authorizers(),
                                   configuration.get_integration)

        if configuration.get_output():
            filename = os.path.join(configuration.get_output(), os.path.basename(filename))
        elif not modified:
            continue
        try:
            with open(filename, "w") as f:
                print(yaml.dump(content, sort_keys=False), file=f)
                print(f"Processed '{filename}'")
        except IOError as iex:
            print(f"Error creating '{filename}' : {iex.strerror}", file=sys.stderr)


if __name__ == '__main__':
    try:
        openapi4aws(Configuration(sys.argv[1:]))
    except ConfigurationError as ex:
        print(ex.args[1], file=sys.stderr)
