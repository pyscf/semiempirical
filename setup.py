#!/usr/bin/env python

NAME         = 'pyscf-semiempirical'
AUTHOR       = 'Qiming Sun'
AUTHOR_EMAIL = 'osirpt.sun@gmail.com'
DESCRIPTION  = 'Semi-empirical methods for PySCF'
#VERSION = '0.0.0'
SO_EXTENSIONS = {'pyscf.lib.libsemiempirical': ['pyscf/semiempirical/repp.c', 'pyscf/semiempirical/rotate.c']}
DEPENDENCIES = ['pyscf', 'numpy']

#######################################################################
# Unless not working, nothing below needs to be changed.
metadata = globals()
import os
import sys
from setuptools import setup, find_namespace_packages, Extension
from setuptools.command.build_ext import build_ext

topdir = os.path.abspath(os.path.join(__file__, '..'))
modules = find_namespace_packages(include=['pyscf.*'])
def guess_version():
    for module in modules:
        module_path = os.path.join(topdir, *module.split('.'))
        for version_file in ['__init__.py', '_version.py']:
            version_file = os.path.join(module_path, version_file)
            if os.path.exists(version_file):
                with open(version_file, 'r') as f:
                    for line in f.readlines():
                        if line.startswith('__version__'):
                            delim = '"' if '"' in line else "'"
                            return line.split(delim)[1]
    raise ValueError("Version string not found")
if not metadata.get('VERSION', None):
    VERSION = guess_version()

pyscf_lib_dir = os.path.join(topdir, 'pyscf', 'lib')
def make_ext(pkg_name, srcs,
             libraries=[], library_dirs=[pyscf_lib_dir],
             include_dirs=[], extra_compile_flags=[],
             extra_link_flags=[], **kwargs):
    if sys.platform.startswith('darwin'):  # OSX
        from distutils.sysconfig import get_config_vars
        conf_vars = get_config_vars()
        conf_vars['LDSHARED'] = conf_vars['LDSHARED'].replace('-bundle', '-dynamiclib')
        conf_vars['CCSHARED'] = " -dynamiclib"
        conf_vars['EXT_SUFFIX'] = '.dylib'
        soname = pkg_name.split('.')[-1]
        extra_link_flags = extra_link_flags + ['-install_name', f'@loader_path/{soname}.dylib']
        runtime_library_dirs = []
    else:
        extra_compile_flags = extra_compile_flags + ['-fopenmp']
        extra_link_flags = extra_link_flags + ['-fopenmp']
        runtime_library_dirs = ['$ORIGIN', '.']
    os.path.join(topdir, *pkg_name.split('.')[:-1])
    return Extension(pkg_name, srcs,
                     libraries = libraries,
                     library_dirs = library_dirs,
                     include_dirs = include_dirs + library_dirs,
                     extra_compile_args = extra_compile_flags,
                     extra_link_args = extra_link_flags,
                     runtime_library_dirs = runtime_library_dirs,
                     **kwargs)

class BuildExtWithoutPlatformSuffix(build_ext):
    def get_ext_filename(self, ext_name):
        from distutils.sysconfig import get_config_var
        ext_path = ext_name.split('.')
        filename = build_ext.get_ext_filename(self, ext_name)
        name, ext_suffix = os.path.splitext(filename)
        return os.path.join(*ext_path) + ext_suffix

settings = {
    'name': metadata.get('NAME', None),
    'version': VERSION,
    'description': metadata.get('DESCRIPTION', None),
    'author': metadata.get('AUTHOR', None),
    'author_email': metadata.get('AUTHOR_EMAIL', None),
    'install_requires': metadata.get('DEPENDENCIES', []),
    'cmdclass': {"build_ext": BuildExtWithoutPlatformSuffix,},
}
if 'SO_EXTENSIONS' in metadata:
    settings['ext_modules'] = [make_ext(k, v) for k, v in SO_EXTENSIONS.items()]
setup(
    include_package_data=True,
    packages=modules,
    **settings
)
