import codefast as cf
from typing import List, Dict, Any, Tuple
import os, subprocess, json
import sys


class Authentication(object):
    """ Authentication with C++.
    """
    @staticmethod
    def run() -> Dict[str, str]:
        bin: str
        stdout: str
        _accounts = {}
        try:
            which_bin = 'bin/dauth' if sys.platform == 'darwin' else 'bin/lauth'
            cmd = os.path.join(cf.io.dirname(), which_bin) + ' -a'
            stdout = subprocess.check_output(
                cmd, shell=True).decode('utf-8').strip()
            _accounts = json.loads(stdout)
        except json.decoder.JSONDecodeError as e:
            cf.io.copy(bin, '/tmp/auth')
            cf.error('failed to decode json {}, '.format(stdout, e))
        except Exception as e:
            cf.error('failed to query secrets: {}'.format(e))
        finally:
            return _accounts


def authc() -> Dict[str, str]:
    return Authentication.run()
