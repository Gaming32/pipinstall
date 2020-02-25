import subprocess

def main(uninstall=False):
    import argparse
    parser = argparse.ArgumentParser()

    def check_version(version):
        if args.no2 and version.startswith(' -2.'):
            return False
        elif args.no3 and version.startswith(' -3.'):
            return False
        elif args.no32 and version.endswith('-32'):
            return False
        elif args.no64 and version.endswith('-64'):
            return False
        return True

    parser.add_argument('packages', metavar='PACKAGE', nargs='+')
    parser.add_argument('-u', '--uninstall', dest='uninstall', action='store_true')
    parser.add_argument('-v', '--verbose', dest='verbose', action='count', default=0)
    parser.add_argument('-q', '--quiet', dest='stdout', action='store_const', const=subprocess.DEVNULL, default=None)
    parser.add_argument('-no2', dest='no2', action='store_true')
    parser.add_argument('-no3', dest='no3', action='store_true')
    parser.add_argument('-no32', dest='no32', action='store_true')
    parser.add_argument('-no64', dest='no64', action='store_true')
    parser.add_argument('--no-pip-update', dest='do_pip_update', action='store_false')
    parser.add_argument('--no-user', dest='do_user', action='store_false')
    parser.add_argument('--no-upgrade', dest='do_upgrade', action='store_false')
    parser.add_argument('--pre', dest='pre', action='store_true')
    parser.add_argument('--force-reinstall', dest='do_reinstall', action='store_true')
    parser.add_argument('--warn-script-location', dest='do_no_warn_script_location', action='store_false')

    args = parser.parse_args()

    uninstall = (uninstall or args.uninstall)
    installcmd = 'un'*uninstall + 'install'
    pythonargs = ['-m', 'pip', installcmd]
    if args.do_user:
        pythonargs.append('--user')
    if args.do_upgrade:
        pythonargs.append('--upgrade')
    if args.pre:
        pythonargs.append('--pre')
    if args.do_reinstall:
        pythonargs.append('--force-reinstall')
    if args.do_no_warn_script_location:
        pythonargs.append('--no-warn-script-location')
    if args.do_pip_update:
        pythonargs.append('pip')
    pythonargs.extend(args.packages)

    if args.verbose >= 2:
        print('Arguments passed to python:', *pythonargs)
    if args.verbose >= 1:
        print('Args to run:', *['py', '-0'])
    process = subprocess.run(['py', '-0'], capture_output=True, text=True)
    pyvers = [x[2:] for x in process.stdout.split('\n')[1:] if check_version(x)]
    if args.verbose >= 2:
        print('Discovered python versions:', *pyvers)

    for version in pyvers:
        print('Installing on version', version)
        command = ['py', '-'+version] + pythonargs
        if args.verbose >= 1:
            print('Args to run:', *command)
        returncode = subprocess.call(command, stdout=args.stdout)
        if returncode:
            print('An error occured with the python version', version, '(The packages were still probably installed, though)')
    print('Done.')

if __name__ == '__main__': main()