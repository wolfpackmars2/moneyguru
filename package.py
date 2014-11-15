# Created By: Virgil Dupras
# Created On: 2009-12-30
# Copyright 2014 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "BSD" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.hardcoded.net/licenses/bsd_license

import os
import os.path as op
import compileall
import shutil
import json
from argparse import ArgumentParser
import platform

from core.app import Application as MoneyGuru
from hscommon.plat import ISWINDOWS, ISLINUX
from hscommon.build import (
    copy_packages, build_debian_changelog, copy_qt_plugins, print_and_do,
    move, copy_all, setup_package_argparser, package_cocoa_app_in_dmg,
    find_in_path
)

def parse_args():
    parser = ArgumentParser()
    setup_package_argparser(parser)
    return parser.parse_args()

def package_windows(dev):
    if not ISWINDOWS:
        print("Qt packaging only works under Windows.")
        return
    from cx_Freeze import setup, Executable
    distdir = 'dist'
    if op.exists(distdir):
        shutil.rmtree(distdir)

    options = {
        'build_exe': {
            'includes': 'atexit',
            'excludes': ['tkinter'],
            'icon': 'images\\main_icon.ico',
            'include_msvcr': True,
        },
        'install_exe': {
            'install_dir': distdir,
        }
    }

    executables = [
        Executable(
            'run.py',
            base='Win32GUI',
            targetDir=distdir,
            targetName='moneyGuru.exe',
        )
    ]

    setup(
        script_args=['install'],
        options=options,
        executables=executables
    )

    if not dev:
        # Copy qt plugins
        plugin_dest = op.join('dist', 'qt4_plugins')
        plugin_names = ['accessible', 'codecs', 'iconengines', 'imageformats']
        copy_qt_plugins(plugin_names, plugin_dest)

    print("Copying forgotten DLLs")
    shutil.copy(find_in_path('msvcp110.dll'), distdir)
    print("Copying the rest")
    shutil.copytree('build\\help', 'dist\\help')
    shutil.copytree('build\\locale', 'dist\\locale')
    shutil.copytree('plugin_examples', 'dist\\plugin_examples')

    if not dev:
        # AdvancedInstaller.com has to be in your PATH
        # this is so we don'a have to re-commit installer.aip at every version change
        shutil.copy('qt\\installer.aip', 'installer_tmp.aip')
        print_and_do('AdvancedInstaller.com /edit installer_tmp.aip /SetVersion %s' % MoneyGuru.VERSION)
        print_and_do('AdvancedInstaller.com /build installer_tmp.aip -force')
        os.remove('installer_tmp.aip')

def copy_files_to_package(destpath, packages, with_so):
    # when with_so is true, we keep .so files in the package, and otherwise, we don't. We need this
    # flag because when building debian src pkg, we *don't* want .so files (they're compiled later)
    # and when we're packaging under Arch, we're packaging a binary package, so we want them.
    if op.exists(destpath):
        shutil.rmtree(destpath)
    os.makedirs(destpath)
    shutil.copy('run.py', op.join(destpath, 'run.py'))
    extra_ignores = ['*.so'] if not with_so else None
    copy_packages(packages, destpath, extra_ignores=extra_ignores)
    shutil.copytree(op.join('build', 'help'), op.join(destpath, 'help'))
    shutil.copytree(op.join('build', 'locale'), op.join(destpath, 'locale'))
    shutil.copy(op.join('images', 'logo_small.png'), destpath)
    shutil.copy(op.join('images', 'logo_big.png'), destpath)
    compileall.compile_dir(destpath)

def package_debian(distribution):
    version = '{}~{}'.format(MoneyGuru.VERSION, distribution)
    destpath = op.join('build', 'moneyguru-{}'.format(version))
    srcpath = op.join(destpath, 'src')
    packages = ['qt', 'hscommon', 'core', 'qtlib', 'plugin_examples', 'sgmllib']
    copy_files_to_package(srcpath, packages, with_so=False)
    shutil.copytree('debian', op.join(destpath, 'debian'))
    move(op.join(destpath, 'debian', 'Makefile'), op.join(destpath, 'Makefile'))
    move(op.join(destpath, 'debian', 'build_modules.py'), op.join(destpath, 'build_modules.py'))
    os.mkdir(op.join(destpath, 'modules'))
    copy_all(op.join('core', 'modules', '*.*'), op.join(destpath, 'modules'))
    build_debian_changelog(
        op.join('help', 'changelog'), op.join(destpath, 'debian', 'changelog'),
        'moneyguru', from_version='1.8.0', distribution=distribution
    )
    os.chdir(destpath)
    cmd = "dpkg-buildpackage -S"
    os.system(cmd)
    os.chdir('../..')

def package_arch():
    # This is called from inside makepkg and gathers what is going to end up in /usr/share/moneyguru
    # in the same folder.
    print("Packaging for Arch")
    srcpath = op.join('build', 'moneyguru-arch')
    packages = ['qt', 'hscommon', 'core', 'qtlib', 'plugin_examples', 'sgmllib']
    copy_files_to_package(srcpath, packages, with_so=True)

def package_source_tgz():
    if not op.exists('deps'):
        print("Downloading PyPI dependencies")
        os.mkdir('deps')
        print_and_do('pip install --download=deps -r requirements.txt setuptools pip')
    app_version = MoneyGuru.VERSION
    name = 'moneyguru-src-{}.tar'.format(app_version)
    dest = op.join('build', name)
    print_and_do('git archive -o {} HEAD'.format(dest))
    print("Adding dependencies and wrapping up")
    print_and_do('tar -rf {} deps'.format(dest))
    print_and_do('gzip {}'.format(dest))

def main():
    args = parse_args()
    conf = json.load(open('conf.json'))
    ui = conf['ui']
    dev = conf['dev']
    if args.src_pkg:
        print("Creating source package for moneyGuru")
        package_source_tgz()
        return
    print("Packaging moneyGuru with UI {0}".format(ui))
    if ui == 'cocoa':
        package_cocoa_app_in_dmg('build/moneyGuru.app', '.', args)
    elif ui == 'qt':
        if ISWINDOWS:
            package_windows(dev)
        elif ISLINUX:
            distname, _, _ = platform.dist()
            if distname == 'arch':
                package_arch()
            else:
                print("Packaging for Ubuntu")
                for distribution in ['trusty', 'utopic']:
                    package_debian(distribution)
        else:
            print("Qt packaging only works under Windows or Linux.")

if __name__ == '__main__':
    main()
