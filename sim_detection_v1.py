import logging
import os
import io
import ntpath


logger = logging.getLogger(__name__)

all_manifests = set()


# find manifest templates in path
"""
finds all manifests in a directory
adds all manifests into add_simhash(filePath string, manifestFile string)
filePath i.e. = templates_of_android_manifest/com.dllingshang.yhb.xml
"""
def find_manifest_templates(cur_dir):
    file_list = []


    for item in os.listdir(cur_dir):
        cur_path = os.path.join(cur_dir, item)
        if os.path.isfile(cur_path):
            file_list.append(cur_path)

    for file in file_list:
        manifestFile = io.open(file, encoding="utf-8").read()
        all_manifests.add(manifestFile)

    print(len(file_list))


#puts all files of templates_of_android_manifest into an index
find_manifest_templates("templates_of_android_manifest/")


def find_duplicates(x):
    if (x in all_manifests):
        return True
    return False


test = io.open("templates_of_android_manifest/a66weding.com.jiehuntong.xml", encoding="utf-8").read()

print(find_duplicates(test))
