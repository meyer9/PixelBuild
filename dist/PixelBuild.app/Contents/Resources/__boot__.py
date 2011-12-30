def _site_packages():
    import site, sys, os
    paths = []
    prefixes = [sys.prefix]
    if sys.exec_prefix != sys.prefix:
        prefixes.append(sys.exec_prefix)
    for prefix in prefixes:
        paths.append(os.path.join(prefix, 'lib', 'python' + sys.version[:3],
            'site-packages'))
    if os.path.join('.framework', '') in os.path.join(sys.prefix, ''):
        home = os.environ.get('HOME')
        if home:
            paths.append(os.path.join(home, 'Library', 'Python',
                sys.version[:3], 'site-packages'))

    # Work around for a misfeature in setuptools: easy_install.pth places
    # site-packages way to early on sys.path and that breaks py2app bundles.
    # NOTE: this is hacks into an undocumented feature of setuptools and
    # might stop to work without warning.
    sys.__egginsert = len(sys.path)

    for path in paths:
        site.addsitedir(path)
_site_packages()


def _chdir_resource():
    import os
    os.chdir(os.environ['RESOURCEPATH'])
_chdir_resource()


def _path_inject(paths):
    import sys
    sys.path[:0] = paths


_path_inject(['/Applications/PixelBuild/Contents'])


def _run(scriptpath):
    global __file__
    import os, sys, site
    sys.frozen = 'macosx_app'
    site.addsitedir(os.environ['RESOURCEPATH'])
    sys.path.append(os.path.dirname(scriptpath))
    sys.argv[0] = __file__ = scriptpath
    execfile(scriptpath, globals(), globals())


try:
    _run('/Applications/PixelBuild/Contents/PixelBuild.py')
except KeyboardInterrupt:
    pass
