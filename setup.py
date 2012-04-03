"""Setup file for packaging swigibpy"""

import os
from distutils.command.build_ext import build_ext
from distutils.core import setup, Extension
from distutils.util import get_platform

###

IB_DIR = 'IB_966'
VERSION = '0.2.3'

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


class swigibpy_build_ext(build_ext):
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


readme = os.path.join(os.path.dirname(__file__), 'README.rst')
setup(version=VERSION,
      name='swigibpy',
      author="Kieran O'Mahony",
      author_email="kieranom@gmail.com",
      url="https://github.com/Komnomnomnom/swigibpy/",
      license='New BSD License',
      description="""Third party Python API for Interactive Brokers""",
      long_description=file(readme).read(),
      keywords=["interactive brokers", "tws"],
      ext_modules=[ib_module],
      py_modules=["swigibpy"],
      cmdclass={'build_ext': swigibpy_build_ext},
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
      )
