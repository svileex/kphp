#!/usr/bin/env python3

import argparse
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description='vkext RPC tests runner')
    parser.add_argument('--engine-repo', required=True, help='path to engine repo')
    parser.add_argument('--valgrind', action='store_true', help='can be run with valgrind')
    args = parser.parse_args()

    if not os.getcwd().endswith('rpc-tests'):
        print('Must be run from vkext/rpc-tests directory')
        return

    engine_repo = os.path.abspath(args.engine_repo)
    kphp_repo = os.path.abspath('../../')
    engine_objs = os.path.join(engine_repo, 'objs/bin')
    kphp_objs = os.path.join(kphp_repo, 'objs/bin')
    tl2php_bin = os.path.join(kphp_objs, 'tl2php')
    rpc_proxy_bin = os.path.join(engine_objs, 'rpc-proxy')
    memcached_bin = os.path.join(engine_objs, 'memcached')
    vkext_so = os.path.join(kphp_repo, 'objs/vkext/modules/vkext.so')
    combined_tlo = os.path.join(engine_objs, 'combined.tlo')

    php_options = '-n -d extension="{}" -d tl.conffile="{}" -d vkext.use_unix=1'.format(vkext_so, combined_tlo)
    valgrind_options = '--log-file=valgrind.out --leak-check=full --show-reachable=yes --track-origins=yes'
    valgrind_env = 'ZEND_DONT_UNLOAD_MODULES=1 USE_ZEND_ALLOC=0'

    subprocess.call(['make', '-j6', 'memcached', 'rpc-proxy'], cwd=engine_repo)
    subprocess.call(['make', '-j6', 'vkext', 'tl2php'], cwd=os.path.join(kphp_repo, 'build'))

    os.system('rm -rf VK')
    os.system('{} {} -i -d .'.format(tl2php_bin, combined_tlo))

    mc = subprocess.Popen([memcached_bin, '-p 5555'])
    rp = subprocess.Popen([rpc_proxy_bin, '-p 4444', 'rpc-proxy.conf'])

    if args.valgrind:
        os.system('{} valgrind {} php {} main.php {}'.format(valgrind_env, valgrind_options, php_options, kphp_repo))
    else:
        os.system('php {} main.php {}'.format(php_options, kphp_repo))

    mc.terminate()
    rp.terminate()


if __name__ == '__main__':
    main()
