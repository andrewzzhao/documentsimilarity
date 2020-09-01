import logging
from simhash import Simhash, SimhashIndex
#import simplejson
import os
#from HashTool import md5sum
import io
#from ApkParser import ApkParser
import ntpath
from sklearn.feature_extraction.text import TfidfVectorizer


logger = logging.getLogger(__name__)

long_manifest_index = SimhashIndex([], k=0)



# find manifest templates in path
"""
finds all manifests in a directory
adds all manifests into add_simhash(filePath string, manifestFile string)
filePath i.e. = templates_of_android_manifest/com.dllingshang.yhb.xml
"""
def find_manifest_templates(cur_dir, manifest, package_name):
    manifest_list = []
    file_list = []

    for item in os.listdir(cur_dir):
        cur_path = os.path.join(cur_dir, item)
        if os.path.isfile(cur_path):
            file_list.append(cur_path)

    for file in file_list:
        manifestFile = io.open(file, encoding="utf-8").read()
        manifest_list.append(manifestFile.lower())

    manifest_list.append(manifest)
    file_list.append("templates_of_android_manifest/a66weding.com.jiehuntong.xml")
    vec = TfidfVectorizer()
    D = vec.fit_transform(manifest_list)
    voc = dict((i, w) for w, i in vec.vocabulary_.items())


    # Verify that distance between data[0] and data[1] is < than
    # data[2] and data[3]
    for i in range(D.shape[0]):
        Di = D.getrow(i)

        # features as list of (token, weight) tuples)
        features = dict(zip([voc[j] for j in Di.indices], Di.data))
        counter += add_simhash(file_list[i], manifestFile, features)


    print(counter)

"""
adds manifest into index with(fileName string, manifest_Hash SimHash object)
"""
def add_simhash(file, manifest, features):
    if manifest:
        manifest_hash = Simhash(features)

        #manifest_hash = Simhash(manifest.split())
        dups = long_manifest_index.get_near_dups(manifest_hash)

        #if dups empty then not dups = true
        if not dups:
            obj_id = ntpath.basename(file).replace('.xml', '')
            long_manifest_index.add(obj_id, manifest_hash)
            message = 'Added id and hash: %s, %s' % (obj_id, manifest_hash.value)
            logger.info(message)
            #return simplejson.dumps({'status': message})
            print({'status': message})
            return 0
        else:
            obj_id = ntpath.basename(file).replace('.xml', '')
            message = 'Failed adding %s Found duplicates: %s' % (obj_id, dups)
            logger.info('add_simhash received manifest:%s, generated hash:%s' % (manifest, manifest_hash.value))
            logger.info(message)
            #return simplejson.dumps({'status': message})
            print({'status': message})
            return 1
    else:
        #return simplejson.dumps({'status': 'Missing required fields'})
        print({'status': 'Missing required fields'})

#puts all files of templates_of_android_manifest into an index
#find_manifest_templates("templates_of_android_manifest/")


def find_duplicates(manifest, package_name):
    find_manifest_templates("templates_of_android_manifest/", manifest, package_name)
    if manifest:
        manifest_length = len(manifest)
        manifest_hash = Simhash(manifest.split())

        print(manifest_hash)

        with open('templates_of_android_manifest/{}.xml'.format(package_name), 'w') as f:
            f.write(manifest)


        dups = long_manifest_index.get_near_dups(manifest_hash)


        long_manifest_index.add(package_name, manifest_hash)

        if dups and package_name not in dups:
            return dups
        else:
            return []
    else:
        return []

# local test
# parser = ApkParser('/Users/jinguo/Documents/t14')
test = io.open("templates_of_android_manifest/a66weding.com.jiehuntong.xml", encoding="utf-8").read()

print(find_duplicates(test, "a66weding.com.jiehuntong"))

# manifestFile = io.open("templates_of_android_manifest/com.dllingshang.yhb.xml", mode="r", encoding="utf-8").read() #open().read()
# print len(manifestFile)
# a = replace_tokens(manifestFile)
# print parser.get_manifest_xml()
# short_manifest_index.add('0', Simhash(a.split()))
# print short_manifest_index.get_near_dups(Simhash(replace_tokens(parser.get_manifest_xml()).split()))
