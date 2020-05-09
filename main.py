import sys
import os
import re
import time
import subprocess
import datetime

class ZoneDomain:
    def __init__(self, folder, domain):
        self._dry_run = False
        self._folder = folder
        self._domain = domain
        self._zone_file = folder + '/' + domain + '.zone'
        self._today_serial = int(datetime.datetime.today().strftime('%Y%m%d00'))

    def cycle_keys(self):

        # TODO: check validity of dnssec for domain
        # TODO: create as items from dnspython

        # subprocess.run(['dnssec-signzone','-S','-r','/dev/urandom','-o',domain,'-t',domain+'.zone'])
        #           + time expire, 3months

        keys = self.dnssec_generate()
        self.write_zone(keys)
        self.gandi_dnssec_call()

        subprocess.run(['dnssec-signzone','-S','-o',domain,'-t',domain+'.zone'])
        subprocess.run(['systemctl','restart','bind9'])

    def read_zone(self):
        with open(self._zone_file, mode='rt', encoding='utf-8') as file:
            self._zone_file_original_content = file.readlines()
        self._preped_content = self._zone_file_original_content.copy()

        for val in self._zone_file_original_content:
            if(val.find('Ser') != -1):
                self._zone_serial = re.search("\d{10}", val)
                if self._zone_serial:
                    self._zone_serial = int(self._zone_serial.group(0))
                break

        for index, val in enumerate(self._preped_content):
            if(val.find('; This is a zone-signing key') != -1 or val.find('; This is a key-signing key') != -1):
                while len(self._preped_content) > index:
                    self._preped_content.pop()

    def dnssec_generate(self):
        [os.rename(file, 'oldkeys/'+file) for file in os.listdir() if (file.startswith('K'+domain))]
        # TODO: Allow different algorithm/bitsize,
        # TODO: Use a python lib to generate those keys
        # #ZSK and KSK

        # TODO : recent versions throws fatal error with -r params

        subprocess.run(['dnssec-keygen','-a','RSASHA512','-b','4096','-n','ZONE', domain])
        # subprocess.run(['dnssec-keygen','-r','/dev/urandom','-a','RSASHA512','-b','4096','-n','ZONE', domain])
        subprocess.run(['dnssec-keygen','-f','KSK','-a','RSASHA512','-b','4096','-n','ZONE', domain])
        # subprocess.run(['dnssec-keygen','-r','/dev/urandom','-f','KSK','-a','RSASHA512','-b','4096','-n','ZONE', domain])
        return [file for file in os.listdir() if (file.startswith('K'+domain) and file.endswith('key'))]

    def write_zone(self, keys):

        # Clean this
        for index, val in enumerate(self._preped_content):
            if(val.find('Ser') != -1):
                i = 0
                while self._zone_serial >= self._today_serial:
                    self._today_serial += 1
                    i += 1
                    if i > 99:
                        raise StopIteration
                self._preped_content[index] = val.replace(str(self._zone_serial), str(self._today_serial))
                break

        for key in keys:
            with open(key, mode='rt', encoding='utf-8') as file:
                self._preped_content.extend([''] + file.readlines() + [''])

        with open(self._zone_file, mode='wt', encoding='utf-8') as file:
            file.writelines(self._preped_content)
        with open(self._zone_file+'.bak', mode='wt', encoding='utf-8') as file:
            file.writelines(self._zone_file_original_content)

    def gandi_dnssec_call(self):
        # api = xmlrpc.client.ServerProxy('https://rpc.gandi.net/xmlrpc/')
        # domain.dnssec.create(apikey, domain, params)
        # v5 of gandi api does not have dnssec keys functionality when using external servers
        pass


def domain_from_folder(folder):
    return folder.split('/')[-1]

if __name__ == '__main__':

    folder = os.getcwd()
    domain = domain_from_folder(folder)
    zone = ZoneDomain(folder,domain)
    zone.read_zone()

    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'run'):
            zone.cycle_keys()
        elif(sys.argv[1] == 'dry-run'):
            zone._dry_run = True
            print('todo')
            exit()
            zone.cycle_keys()
        else:
            print('print help')
