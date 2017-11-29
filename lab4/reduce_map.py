from multiprocessing import Pool
"""given the [(word_id, doc_id),(word_id, doc_id),...]"""
class reduce_map(object): # purpose, build the inverted_index

    def __init__(self, lst): # a list of tuples
        self.word_doc_lst = lst
        self.partitioned_text = []
        self.inverted_index = {}

    def chunks(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    def Partition(self, L):  #L is results list  [(word_id, doc_id),(word_id, doc_id),...]
        tf = {}
        for sublist in L:
            for p in sublist:
                try:
                    tf[p[0]].append(p)
                except KeyError:
                    tf[p[0]] = [p]
        return tf   # tf{word_id:[(word_id, doc_id1),(word_id, doc_id2),...]; word_id:]}

# Build a pool of 8 processes

    def red_map(self):
        partitioned_id = list(self.chunks(self.word_doc_lst, len(self.word_doc_lst) / 8))  # a list of [(),(),..]
        word_to_doc = self.Partition(partitioned_id)  # get a dictionary
        pool = Pool(processes=8, )
        x = pool.map(Reduce, list(zip(word_to_doc, word_to_doc.values())))
        return x

def Reduce(Mapping):  # Mapping is the tuple(word_i,[(word_id, doc_id),(word_id, doc_id)])
    inverted_index = {}
    inverted_index[Mapping[0]] = {pair[1] for pair in Mapping[1]}  # set comprehesion
    return (inverted_index)


if __name__ == "__main__":
    l = [(1,3), (2,3), (4,2),(1,3), (2,3), (4,2),(1,3), (2,3), (4,2),(1,3), (2,3), (4,2)]
    bot = reduce_map(l)
    x = bot.red_map()
    print(x)
