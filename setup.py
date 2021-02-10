#!/usr/bin/env python

import os
from setuptools import setup, Extension
import setuptools.command.install

__base__ = {
    'name':'midi3',
    'version':'v0.0.1',
    'description':'Python MIDI API',
    'author':'giles hall, adam suki',
    'author_email':'ghall@csh.rit.edu, outlyingdo@gmail.com',
    'package_dir':{'midi3':'src'},
    'py_modules':['midi3.containers', 'midi3.__init__', 'midi3.events', 'midi3.util', 'midi3.fileio', 'midi3.constants'],
    'ext_modules':[],
    'ext_package':'',
    'scripts':['scripts/mididump.py', 'scripts/mididumphw.py', 'scripts/midiplay.py'],
}

# this kludge ensures we run the build_ext first before anything else
# otherwise, we will be missing generated files during the copy
class Install_Command_build_ext_first(setuptools.command.install.install):
    def run(self):
        self.run_command("build_ext")
        return setuptools.command.install.install.run(self)

def setup_alsa(ns):
    # scan for alsa include directory
    dirs = ["/usr/include", "/usr/local/include"]
    testfile = "alsa/asoundlib.h"
    alsadir = None
    for _dir in dirs:
        tfn = os.path.join(_dir, testfile)
        if os.path.exists(tfn):
            alsadir = _dir
            break
    if not alsadir:
        print("Warning: could not find asoundlib.h, not including ALSA sequencer support!")
        return
    srclist = ["src/sequencer_alsa/sequencer_alsa.i"]
    include_arg = "-I%s" % alsadir
    extns = {
        'libraries': ['asound'],
        'swig_opts': [include_arg],
        #'extra_compile_args':['-DSWIGRUNTIME_DEBUG']
    }
    ext = Extension('_sequencer_alsa', srclist, **extns)
    ns['ext_modules'].append(ext)

    ns['package_dir']['midi3.sequencer'] = 'src/sequencer_alsa'
    ns['py_modules'].append('midi3.sequencer.__init__')
    ns['py_modules'].append('midi3.sequencer.sequencer')
    ns['py_modules'].append('midi3.sequencer.sequencer_alsa')
    ns['ext_package'] = 'midi3.sequencer'
    ns['cmdclass'] = {'install': Install_Command_build_ext_first}

def configure_platform():
    from sys import platform
    ns = __base__.copy()
    # currently, only the ALSA sequencer is supported
    if platform.startswith('linux'):
        setup_alsa(ns)
        pass
    else:
        print("No sequencer available for {} platform.".format(platform))
    return ns

if __name__ == "__main__":
    setup(**configure_platform())


