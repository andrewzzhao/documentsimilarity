import logging
from simhash import Simhash, SimhashIndex
#import simplejson
import os
#from HashTool import md5sum
import io
#from ApkParser import ApkParser
import ntpath


logger = logging.getLogger(__name__)

short_manifest_index = SimhashIndex([], k=1)
medium_manifest_index = SimhashIndex([], k=2)
long_manifest_index = SimhashIndex([], k=3)

replace_dict = {
    'manifest': '1',
    'uses-sdk': '2',
    'uses-permission': '3',
    'application': '4',
    'activity': '5',
    'intent-filter': '6',
    'category': '7',
    'service': '8',
    'supports-screens': '9',
    '<?xml version="1.0" ?>': '',
    'android:versionCode': '10',
    'android:versionName': '11',
    'android:icon': '12',
    'android:label': '13',
    'android:name': '14',
    'android:theme': '15',
    'android:screenOrientation': '16',
    'android:configChanges': '17',
    'android:debuggable': '18',
    'android:launchMode': '19',
    'android:minSdkVersion': '20',
    'xmlns:android="http://schemas.android.com/apk/res/android"': '',
    'android.permission': '21',
    'action': '22',
    'android.intent': '23',
    'android:targetSdkVersion': '24',
    'android:windowSoftInputMode': '25',
}


def replace_tokens(manifest):
    for k, v in replace_dict.items():
        manifest = manifest.replace(k, v)
    return manifest


# find manifest templates in path
def find_manifest_templates(cur_dir):
    file_list = []

    for item in os.listdir(cur_dir):
        cur_path = os.path.join(cur_dir, item)
        if os.path.isfile(cur_path):
            file_list.append(cur_path)

    for file in file_list:
        manifestFile = io.open(file, encoding="utf-8").read()
        add_simhash(file, manifestFile)


def add_simhash(file, manifest):
    if manifest:
        manifest_hash = Simhash(replace_tokens(manifest).split())
        dups = long_manifest_index.get_near_dups(manifest_hash)

        if not dups:
            obj_id = ntpath.basename(file).replace('.xml', '')
            short_manifest_index.add(obj_id, manifest_hash)
            medium_manifest_index.add(obj_id, manifest_hash)
            long_manifest_index.add(obj_id, manifest_hash)
            message = 'Added id and hash: %s, %s' % (obj_id, manifest_hash.value)
            logger.info(message)
            print({'status': message})
        else:
            message = 'Failed adding. Found duplicates: %s' % dups
            logger.info('add_simhash received manifest:%s, generated hash:%s' % (manifest, manifest_hash.value))
            logger.info(message)
            print({'status': message})
    else:
        print({'status': 'Missing required fields'})


find_manifest_templates("templates_of_android_manifest/")


def find_duplicates(manifest, package_name):
    if manifest:
        manifest_length = len(manifest)
        manifest_hash = Simhash(replace_tokens(manifest).split())

        with open('templates_of_android_manifest/{}.xml'.format(package_name), 'w') as f:
            f.write(manifest)

        short_manifest_threshold = 2048
        long_manifest_threshold = 4096

        if manifest_length < short_manifest_threshold:
            dups = short_manifest_index.get_near_dups(manifest_hash)
        elif manifest_length > long_manifest_threshold:
            dups = long_manifest_index.get_near_dups(manifest_hash)
        else:
            dups = medium_manifest_index.get_near_dups(manifest_hash)

        short_manifest_index.add(package_name, manifest_hash)
        medium_manifest_index.add(package_name, manifest_hash)
        long_manifest_index.add(package_name, manifest_hash)

        if dups and package_name not in dups:
            return dups
        else:
            return []
    else:
        return []


test = io.open("templates_of_android_manifest/a66weding.com.jiehuntong.xml", encoding="utf-8").read()

print(find_duplicates(test, "a66weding.com.jiehuntong"))
# local test
# parser = ApkParser('/Users/jinguo/Documents/t14')

# manifestFile = io.open("templates_of_android_manifest/com.dllingshang.yhb.xml", mode="r", encoding="utf-8").read() #open().read()
# print len(manifestFile)
# a = replace_tokens(manifestFile)
# print parser.get_manifest_xml()
# short_manifest_index.add('0', Simhash(a.split()))
# print short_manifest_index.get_near_dups(Simhash(replace_tokens(parser.get_manifest_xml()).split()))
