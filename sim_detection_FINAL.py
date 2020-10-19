import logging
from simhash import Simhash, SimhashIndex
import os
import io
import ntpath
from sklearn.feature_extraction.text import TfidfVectorizer
#import simplejson


logger = logging.getLogger(__name__)

long_manifest_index = SimhashIndex([], k=5)



# find manifest templates in path
"""
finds all manifests in a directory
adds all manifests into add_simhash(filePath string, manifestFile string)
filePath i.e. = templates_of_android_manifest/com.dllingshang.yhb.xml
"""
def find_duplicates_helper(cur_dir, manifest, package_name):
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
    file_list.append(package_name)
    vec = TfidfVectorizer()
    D = vec.fit_transform(manifest_list)
    voc = dict((i, w) for w, i in vec.vocabulary_.items())


    for i in range(D.shape[0]):
        Di = D.getrow(i)

        # features as list of (token, weight) tuples)
        features = dict(zip([voc[j] for j in Di.indices], Di.data))
        if(i != D.shape[0] - 1):
            add_simhash(file_list[i], manifestFile, features)
        else:
            manifest_hash = Simhash(features)
            dups = long_manifest_index.get_near_dups(manifest_hash)

    #if dups empty then not dups = true
    if not dups:
        long_manifest_index.add(package_name, manifest_hash)
        print "no similar documents found"
        return []
    else:
        message = 'File Name: %s Found duplicates: %s' % (package_name, dups)
        print {'status': message}
        return dups


"""
adds manifest into index with(fileName string, manifest_Hash SimHash object)
"""
def add_simhash(file, manifest, features):
    if manifest:
        manifest_hash = Simhash(features)
        long_manifest_index.add(ntpath.basename(file).replace('.xml', ''), manifest_hash)

    else:
        print {'status': 'Missing required fields'}



def find_duplicates(manifest, package_name):
    return find_duplicates_helper("templates_of_android_manifest/", manifest, package_name)


test = io.open("a66weding.com.jiehuntong.xml", encoding="utf-8").read()

print find_duplicates(test, "a66weding.com.jiehuntong") 
