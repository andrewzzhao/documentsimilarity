# assuming that you have a dictionary with document id as the key and the document as the value:
# documents = { doc_id: doc } you can do:
from simhash import simhash

documents = { 1 : open('first.txt', 'r').read() , 2 : open('second.txt', 'r').read(), 3 : open('Tests/third.txt', 'r').read(), 4 : open('Tests/fourth.txt', 'r').read()}

def split_hash(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

hashes = {}
for doc_id, doc in documents.items():
    print(doc_id)
    print(doc)
    hash = simhash(doc)

    # you can either use the whole hash for higher precision or split into chunks for higher recall
    hash_chunks = split_hash(hash, 4)

    for chunk in hash_chunks:
        if chunk not in hashes:
            hashes[chunk] = []
        hashes[chunk].append(doc_id)

# now you can print the duplicate documents:
for hash, doc_list in hashes:
    if doc_list > 1:
        print("Duplicates documents: ", doc_list)
