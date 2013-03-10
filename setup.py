"""Setup file for packaging swigibpy"""

import re
import sys
from os import system, chdir, getcwd, listdir
from os.path import join, dirname, abspath
from sysconfig import get_platform

try:
    from setuptools.command.build_ext import build_ext
    from setuptools import setup, Extension, Command
    _have_setuptools = True
except:
    from distutils.command.build_ext import build_ext
    from distutils import setup, Extension, Command
    _have_setuptools = False

###

IB_DIR = 'IB'
VERSION = '0.4'

root_dir = abspath(dirname(__file__))
libraries = []

setuptools_kwargs = {}
if sys.version_info[0] >= 3:
    setuptools_kwargs = {'use_2to3': True}
    if not _have_setuptools:
        sys.exit("need setuptools/distribute for Py3k"
                 "\n$ pip install distribute")

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
                '-outdir ' + root_dir,
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
        system('swig ' + ' '.join(self.swig_opts) +
               ' -o swig_wrap.cpp ' + join(root_dir, 'swigify_ib.i'))

        print('Removing boost namespace')

        # Remove boost namespace, added to support IB's custom shared_ptr
        with open(join(root_dir, IB_DIR, 'swig_wrap.cpp'), 'r+') as swig_wrap:
            contents = swig_wrap.read()
            contents = contents.replace("boost::shared_ptr", "shared_ptr")
            contents = re.sub(
                    r'(shared_ptr<[^>]+>\([^)]+ )(SWIG_NO_NULL_DELETER_0)\)',
                    r'\1)',
                    contents
                    )
            swig_wrap.seek(0)
            swig_wrap.truncate()
            swig_wrap.write(contents)
        chdir(self.cwd)


class Patchify(Command):
    description = "Apply swigibpy's patches to the TWS API"
    user_options = [
            ('reverse', 'r', 'Un-apply the patches')
            ]

    def initialize_options(self):
        self.cwd = None
        self.reverse = False
        self.patch_opts = []

    def finalize_options(self):
        self.cwd = getcwd()
        if self.reverse:
            self.patch_opts.append('-R')

    def run(self):
        chdir(root_dir)
        for patch in listdir(join(root_dir, 'patches')):
            system('git apply ' + ' '.join(self.patch_opts) + ' ' +
                   join(root_dir, 'patches', patch))
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


readme = join(dirname(__file__), 'README.rst')
setup(version=VERSION,
      name='swigibpy',
      author="Kieran O'Mahony",
      author_email="kieranom@gmail.com",
      url="https://github.com/Komnomnomnom/swigibpy/",
      license='New BSD License',
      description="""Third party Python API for Interactive Brokers""",
      long_description=open(readme).read(),
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
          "Programming Language :: Python :: 2.6",
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Office/Business :: Financial",
          ],
      **setuptools_kwargs
      )
