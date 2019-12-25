from __future__ import absolute_import, print_function
from .common import *
from zipfile import ZipFile

__version__ = '0.2.0'

msvc_batch = '''
set PATH={};%PATH%
set DEPOT_TOOLS_WIN_TOOLCHAIN=0

call run_gclient.bat

git clone https://chromium.googlesource.com/angle/angle
cd angle
python scripts/bootstrap.py
gclient sync
git checkout master

call "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Enterprise\\Common7\\Tools\\VsDevCmd.bat"

gn gen out/Release --args='is_debug=false target_cpu="{}"'

autoninja -C out\\Release libEGL
autoninja -C out\\Release libGLESv2
'''


def get_angle(cache, build_path, arch, package, output, download_only=False):
    url = 'https://storage.googleapis.com/chrome-infra/depot_tools.zip'
    local_url = download_cache(cache, url, build_path)
    if download_only:
        return

    print('Extracting {}'.format(local_url))
    with open(local_url, 'rb') as fd:
        ZipFile(fd).extractall(join(build_path, package, 'depot_tools'))

    base_dir = join(build_path, package)
    batch = msvc_batch.format(
        join(base_dir, 'depot_tools'), arch)

    with open(join(base_dir, 'run_gclient.bat'), 'w') as fh:
        fh.write('gclient\nexit /b 0')

    with open(join(base_dir, 'compile.bat'), 'w') as fh:
        fh.write(batch)
    exec_binary('', [join(base_dir, 'compile.bat')], cwd=base_dir, shell=True)

    data = []
    out_dir = join(base_dir, 'angle', 'out', 'Release')
    for dll in ('libEGL.dll', 'libGLESv2.dll', 'd3dcompiler_47.dll'):
        data.append((join(out_dir, dll), join('bin', dll),
                     join('share', package, 'bin'), False))

    make_package(join(build_path, 'project'), package, data, __version__, output, 'MIT')


if __name__ == '__main__':
    parse_args(get_angle)
