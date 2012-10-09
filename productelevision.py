#!/usr/bin/env python
# Record a movie of your computer use, to see how productive your day was!
#   Based on a script by jamak (gist 3068171); I'm just too lazy/inept to
#   install zsh. Also something about an OS X screenshot utility. Yes.
#
# P.S. It takes a lot of granola to turn a 22 line shell script into a
#   50+ line Python program

import subprocess, random, string, time

utils = {
    'screenshot': '/usr/bin/scrot -q 50 -m -z {path}/{num:07}.png',
    'movie': 'avconv -f image2 -qscale 2 -same_quant -i {path}/%07d.png {path}/output.mpeg'
}

def observe_user(output_dir):
    period = 16 #seconds

    cur = 0
    done = False
    while not done:
        err = subprocess.call(utils['screenshot'].format(
                path=output_dir, num=cur), shell=True)
        if err != 0:
            raise EnvironmentError(err, 'screenshot call failed')
        cur += 1
        try:
            time.sleep(period)
        except KeyboardInterrupt:
            done = True

def movie_from_images(input_dir):
    err = subprocess.call(utils['movie'].format(path=input_dir), shell=True)
    if err != 0:
        raise EnvironmentError(err, 'movie compile call failed')


def main(output_dir):
    err = subprocess.call(['mkdir', output_dir])
    if err != 0:
        raise EnvironmentError(err, 'cannot make output directory')
    observe_user(output_dir)
    movie_from_images(output_dir)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('USAGE: {} output_directory'.format(sys.argv[0]))
    main(sys.argv[1])
