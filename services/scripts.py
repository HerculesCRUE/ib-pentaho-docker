import subprocess
import time
import requests

class BASH:

    def __init__(self):
        self.this = self

    def start_environment(self,limit):
        self.stop_environment()
        print('DEPLOYING SANDBOX.....')
        subprocess.call('sh ./docker-env/sandbox/start-sandbox.sh')
        return self.wait_until_deploy(limit)

    def stop_environment(self):
        print('SANDBOX ENVIRONMENT.....')
        subprocess.call('sh ./docker-env/sandbox/stop-sandbox.sh')
        print('SANDBOX IS STOPPED')

    def wait_until_deploy(self,limit):
        steps = 5
        limit = limit
        deployed = False
        for i in range(0, limit, steps):
            if self.__check_uris_factory_health():
                deployed = True
                break
            else:
                print('\t...environment not yet deployed, waiting %s seconds to reach the limit of %s seconds' % ((limit-i),limit))
                time.sleep(steps)
        if deployed:
            print('SANDBOX IS DEPLOYED............CONGRATULATIONS!!!!')
        else:
            print('SANDBOX DEPLOY FAIL, PLEASE TRY AGAIN')
        return deployed


    def __check_uris_factory_health(self):
        try:
            response = requests.get('http://localhost:9326/management/health')
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False