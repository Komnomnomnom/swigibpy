"""Setup file for packaging swigibpy"""

import re
import subprocess
import sys
from os import chdir, getcwd, listdir
from os.path import join, dirname, abspath
from sysconfig import get_platform

try:
    from setuptools.command.build_ext import build_ext
    from setuptools import setup, Extension, Command
except:
    from distutils.command.build_ext import build_ext
    from distutils import setup, Extension, Command

###

IB_DIR = 'IB'
VERSION = '0.4'

root_dir = abspath(dirname(__file__))
libraries = []

if(get_platform().startswith('win')):
    libraries.append('ws2_32')

ib_module = Extension('_swigibpy',
                      sources=[IB_DIR +
                               '/PosixSocketClient/EClientSocketBase.cpp',
                               IB_DIR +
                               '/PosixSocketClient/EPosixClientSocket.cpp',
                               IB_DIR + '/swig_wrap.cpp'],
                      include_dirs=[IB_DIR,
                                    IB_DIR + '/PosixSocketClient',
                                    IB_DIR + '/Shared'],
                      define_macros=[('IB_USE_STD_STRING', '1')],
                      libraries=libraries
                      )


class Swigify(Command):
    description = "Regenerate swigibpy's wrapper code (requires SWIG)"
    user_options = []

    def initialize_options(self):
        self.swig_opts = None
        self.cwd = None

    def finalize_options(self):
        self.cwd = getcwd()
        self.swig_opts = [
                '-v',
                '-c++',
                '-python',
                '-threads',
                '-keyword',
                '-w511',
                '-outdir',
                root_dir,
                '-modern',
                '-fastdispatch',
                '-nosafecstrings',
                '-noproxydel',
                '-fastproxy',
                '-fastinit',
                '-fastunpack',
                '-fastquery',
                '-modernargs',
                '-nobuildnone'
                ]

    def run(self):
        chdir(join(root_dir, IB_DIR))
        try:
            swig_cmd = ['swig'] + self.swig_opts + ['-o', 'swig_wrap.cpp']
            swig_cmd.append(join(root_dir, 'swigify_ib.i'))
            subprocess.check_call(swig_cmd)

            print('Removing boost namespace')

            # Remove boost namespace, added to support IB's custom shared_ptr
            swig_files = [
                join(root_dir, IB_DIR, 'swig_wrap.cpp'),
                join(root_dir, IB_DIR, 'swig_wrap.h'),
                join(root_dir, 'swigibpy.py')
                ]

            for swig_file in swig_files:
                with open(swig_file, 'r+') as swig_file_handle:
                    contents = swig_file_handle.read()
                    contents = contents.replace(
                            "boost::shared_ptr", "shared_ptr")
                    contents = re.sub(
                        r'(shared_ptr<[^>]+>\([^)]+ )'
                            r'(SWIG_NO_NULL_DELETER_0)\)',
                        r'\1)',
                        contents
                        )
                    swig_file_handle.seek(0)
                    swig_file_handle.truncate()
                    swig_file_handle.write(contents)
        except subprocess.CalledProcessError as cpe:
            pass
        finally:
            chdir(self.cwd)


class Patchify(Command):
    description = "Apply swigibpy's patches to the TWS API"
    user_options = [
            ('reverse', 'r', 'Un-apply the patches')
            ]

    def initialize_options(self):
        self.cwd = None
        self.reverse = False
        self.patch_opts = ['-v']

    def finalize_options(self):
        self.cwd = getcwd()
        if self.reverse:
            self.patch_opts.append('-R')

    def run(self):
        chdir(root_dir)
        for patch in listdir(join(root_dir, 'patches')):
            patch_cmd = ['git', 'apply'] + self.patch_opts
            patch_cmd.append(join(root_dir, 'patches', patch))
            subprocess.call(patch_cmd)
        chdir(self.cwd)


class SwigibpyBuildExt(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        if compiler == 'msvc':
            extra = ('/D_CRT_SECURE_NO_DEPRECATE',
                     '/EHsc', '/wd4355', '/wd4800')
        else:
            extra = ('-Wno-switch',)
        for ext in self.extensions:
            ext.extra_compile_args += extra
        build_ext.build_extensions(self)


readme = open(join(root_dir, 'README.rst'))
setup(version=VERSION,
      name='swigibpy',
      author="Kieran O'Mahony",
      author_email="kieranom@gmail.com",
      url="https://github.com/Komnomnomnom/swigibpy/",
      license='New BSD License',
      description="""Third party Python API for Interactive Brokers""",
      long_description=readme.read(),
      keywords=["interactive brokers", "tws"],
      ext_modules=[ib_module],
      py_modules=["swigibpy"],
      cmdclass={
          'build_ext': SwigibpyBuildExt,
          'swigify': Swigify,
          'patchify': Patchify,
          },
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Office/Business :: Financial",
          ],
      )
readme.close()
