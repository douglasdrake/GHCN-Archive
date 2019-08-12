# GHCN archive class

import os
from six.moves import urllib
import tarfile
#import urllib2

GHCN_PATH = os.path.join("static", "src")
GHCN_URL = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/"
GHCN_FILES = {
    'GHCN_TGZ': "ghcnd_all.tar.gz",
    'GHCN_VERSION': "ghcnd-version.txt",
    'GHCN_STATIONS': "ghcnd-stations.txt",
    'GHCN_INVENTORY': "ghcnd-inventory.txt",
    'GHCN_COUNTRIES': "ghcnd-countries.txt",
    'GHCN_STATES': "ghcnd-states.txt",
    'GHCN_DAILY': os.path.join(GHCN_PATH, 'ghcnd_all')}

class GHCN_archive:
    def __init__(self, ghcn_url=GHCN_URL, ghcn_path=GHCN_PATH):
        self.url = ghcn_url
        self.path = ghcn_path
        self.files = GHCN_FILES
        self.version_file = os.path.join(self.path, self.files['GHCN_VERSION'])
        self.init_complete = False
        self.setup_complete = False
        self.version = None
        self.extracts = []
        
        # check if the path exists - if not setup the directory structure
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        else:
            # see if the archive is already downloaded
            self.check_setup()
            if self.setup_complete:
                self.set_version()
            # see if any files already extracted
            if os.path.isdir(self.files['GHCN_DAILY']):
                self.extracts = os.listdir(self.files['GHCN_DAILY'])
                    
        # check if the url given is valid
        try:
            site = urllib.request.urlopen(ghcn_url)
            self.init_complete = True
        except Exception as e:
            print(e)
            print(f'URL {ghcn_url} is not valid')
            self.init_complete = False
            
    def __repr__(self):
        return (f'{self.__class__.__name__}(Initialized: {self.init_complete}, Setup: {self.setup_complete}, Version: {self.version})')

    def check_setup(self):
        # see if all six files are already downloaded, if True - set setup flag to True
        for item in list(self.files.values())[:-1]:
            fname = os.path.join(self.path, item)
            print(f"Checking: {fname}")
            if not os.path.isfile(fname):
                self.setup_complete = False
                print(f"Setup failed for: {fname}")
                return
        # only get to here if all 6 files are downloaded
        self.setup_complete = True
        
    def set_version(self):
        if os.path.isfile(self.version_file):
            with open(self.version_file, 'r') as fp:
                version_list = []
                for line in fp:
                    version_list.extend(line.split())
                self.version = version_list[7] # this uses specific information about the file structure of `ghcnd-inventory.txt`
                print(f"Version found: {self.version}")
        else:
            self.version = None
            print("No local version found")
        
    def setup(self):
        # download the six files 
        # change the setup_complete flag to False if fail to download any of the 6 files
        self.setup_complete = True 
        for item in list(self.files.values())[:-1]:
            item_url = self.url + item
            item_path = os.path.join(self.path, item)
            try:
                print(f"Downloading {item_url}")
                urllib.request.urlretrieve(item_url, item_path)
                # set the version
                if item_path == self.version_file:
                    self.set_version()
            except Exception as e:
                print(e)
                print(f"Failed to download the file: {item}")
                self.setup_complete = False
        
    def remove_archive(self):
        # removes the files but keeps the directory structure
        for item in list(self.files.values()):
            item_path = os.path.join(self.path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                
        # remove any extracted files
        for item in self.extracts:
            item_path = os.path.join(self.files['GHCN_DAILY'], item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        
        if os.path.exists(self.files['GHCN_DAILY']):
            os.rmdir(self.files['GHCN_DAILY'])
            
        self.setup_complete = False
        self.extracts = []
        self.version = None
            
    def check_for_newer_version(self):
        # download the version file and compare to file on location
        if self.version:
            tmp_version = os.path.join(self.path, "tmp_version.txt")
            version_url = self.url + self.files['GHCN_VERSION']
            try:
                urllib.request.urlretrieve(version_url, tmp_version)
            except Exception as e:
                print(e)
                print(f"Failed to retrieve version file: {version_url}")
            
            if os.path.isfile(tmp_version):
                with open(tmp_version, 'r') as fp:
                    version_list = []
                    for line in fp:
                        version_list.extend(line.split())
                    newest_version = version_list[7]
                    print(f"Current version: {self.version}; Newest versison: {newest_version}")
                os.remove(tmp_version)
        else:
            print(f"No local version available")
            
    def list_files(self):
        files = os.listdir(self.path)
        for file in files:
            print(file)
        if self.extracts:
            for file in self.extracts:
                print(file)

    def extract_station(self, station_id):
        if not self.setup:
            print(f"Archive not setup.  Create archive first.")
            return
        tgz_file = os.path.join(self.path, self.files['GHCN_TGZ'])
        tar = tarfile.open(tgz_file, 'r:gz')
        dly_file = "ghcnd_all/" + station_id + ".dly"
        outdir = self.path
        try:
            tar.extract(dly_file, outdir)
            self.extracts.append(station_id + '.dly')
        except Exception as e:
            print(e)
        tar.close()
        
    def extract_stations(self, station_ids):
        if not self.setup:
            print(f"Archive not setup.  Create archive first.")
            return
        tgz_file = os.path.join(self.path, self.files['GHCN_TGZ'])
        tar = tarfile.open(tgz_file, 'r:gz')
        for station_id in station_ids:
            dly_file = "ghcnd_all/" + station_id + ".dly"
            outdir = self.path
            try:
                tar.extract(dly_file, outdir)
                self.extracts.append(station_id + '.dly')
            except Exception as e:
                print(e)
                print(f"Failed to extract {dly_file}")
        tar.close()