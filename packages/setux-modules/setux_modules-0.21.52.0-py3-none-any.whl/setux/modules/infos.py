from setux.core import __version__
from setux.logger import logger, info
from setux.core.module import Module


class Distro(Module):
    '''Show target infos
    '''
    def deploy(self, target, **kw):
        user = target.login.name
        kernel = target.kernel
        python = target.run('python3 -V')[1][0]
        with logger.quiet():
            try:
                addr = target.net.addr
            except:
                addr = '!'

        infos =  f'''
        target : {target}
        distro : {target.distro.name}
        python : {python}
        os     : {kernel.name} {kernel.version} / {kernel.arch}
        user   : {user}
        host   : {target.system.hostname} : {addr}
        setux  : {__version__}
        '''

        info(infos)

        return True
