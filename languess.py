from operator import itemgetter
import re

def strcmp(s1, s2):
    """
        strcmp

        This function is similar function to the C strcmp, but for
        our need it works in an inverted way.

        If you're using this to sort a string's list it will be sorted reversed.
    """
    i = 0
    if s1 > s2:
        return 1
    elif s1 == s2:
        return 0
    else:
        return -1

class MyError(Exception):
    """
        Simple foobar-like error class
    """
    def __init__(self, value):
        self.value = value  
    def __str__(self):
        return repr(self.value)


def train(source, out=None, utf8=True):
    """
        Train

        This function creates the knowledge from a sample(source)
        and store it into the knowledge file (out) or return it as a list

        Internally we manage with utf-8, and it assumes that your 
        data sample is in UTF-8.
    """
    text = "\n".join([line for line in open(source).readlines()])
    if utf8 == False:
        text = text.decode("iso-8859-1").encode("utf-8")
    lg = Languess()
    # we got the n-grams sorted alphabetically for fast
    # comparition, but it we need it sorted by its ranking
    # so here he sort it
    ngrams = [(v,k) for (k, v) in lg.ngrams(text,400)]
    ngrams.sort()
    if out != None:
        f = open(out,"w+b")
        for (k,v) in ngrams:
            f.write(v)
            f.write("\n")
        f.close()
    else:
        return ngrams


class Languess():
    """
        Language Guesser class.

        Simple class that aims to guess the language from given text.

        The system must be train with samples previously.
    """
    __knowledge = [] 
    threshold   = 1.001
    maxresult   = 5
    ngramsize   = 400
    MAXSCORE    = 401

    def outofplace(self, arr1, arr2, cutoff):
        """
            A simple function to measure the text n-gram
            table against our "knowledge" n-gram table.
        """
        i = e = 0
        mi, me = len(arr1), len(arr2)

        dist = 0
        while (i < mi and e < me):
            cmp = strcmp(arr1[i][0], arr2[e][0])
            if cmp < 0:
                i+=1
            elif cmp == 0:
                dist += abs(arr1[i][1] - arr2[e][1])
                if (dist > cutoff):
                    return False
                i+=1
                e+=1
            else:
                dist += self.MAXSCORE
                if dist > cutoff:
                    return False
                e+=1

        while e < me:
            dist += self.MAXSCORE
            if dist > cutoff:
                return False
            e += 1

        return dist

    def getLang(self, text):
        """
            Get Language

            This method returns the language from a given text.
        """
        kledge    = self.__knowledge
        threshold = 2147483647
        minscore  = threshold
        cands     = []

        if len(kledge) == 0:
            raise MyError("No knowledge loaded.")

        ngrams  = self.__get_ngrams(text, self.ngramsize)

        if len(ngrams) < 50:
            raise MyError("Text too short") 

        # Loop over the knowledges and find the one 
        # which seems more similar
        for lang in kledge:
            dist = self.outofplace(lang[1], ngrams, threshold)
            if dist == False:
                continue
            cands.append( (lang[0], dist) )
            #print "%d %d %s" % (dist, threshold, lang)
            if dist < minscore:
                minscore  = dist
                threshold = int(dist * self.threshold)

        # Delete all those candidates that are 
        # out from the threshold
        results = []
        for (lang, score) in cands:
            if threshold > score:
                results.append( (lang, score) )

        if len(results) == 1:
            return [(results[0][0],100)]

        # we got some results, sort it, and return the score
        # in a percentaje fashion
        return [(lang, self.__get_rscore(score)) for (lang,score) in sorted(results,key=itemgetter(1)) ]


    def __get_rscore(self, score):
        """
            Odd function to represent the score in a greater fashion.
        """
        return (1-(score/float(self.MAXSCORE * self.ngramsize) )) * 100

    def load_knowledge(self, knowledge):
        """
            This functions loads the knowledge files, and prepare it
            for fast comparition.
        """
        tmp = []
        for k in knowledge.items():
            ngrams = []
            i=0;
            for ngram in k[1]:
                ngrams.append((ngram,i))
                i+=1
            tmp.append((k[0], sorted(ngrams, key=itemgetter(0))))
        self.__knowledge =  tmp

    def __ngram_sort(self, a, b):
        """
            Custom simple function used for ngrams' sorting
        """
        if a[1] > b[1]:
            return -1
        if a[1] < b[1]:
            return 1
        return strcmp(a[0], b[0])

    def __get_ngrams(self,text, n):
        """ 
            Get n-grams

            This function is the head of this project. It extract n-grams
            from a given text and return a list of tuples (ngram, ranking) sorted
            alphabetically by ngrams. 
        """
        ngrams = {} 
        # cleaning text
        text  = re.sub("[\[\]\(\)\,\t\.0-9\?]","",text.lower())
        text  = re.sub("\s+","_",text)
        text  = "_%s_" % text
        ltext = len(text)

        #  extract all the n-grams
        #  spaces are allowed only on the borders.
        x = 0
        for i in range(ltext):
            for e in range(1,6):
                if i+e == ltext:
                    break
                word = text[ i : i + e ]
                if not ngrams.has_key(word):
                    ngrams[ word ] = 0
                ngrams[ word ] += 1
                if e > 1 and word[-1] == '_':
                    break
   
        # some little trick in order to order the sort
        tmp = ngrams.items()
        tmp.sort(self.__ngram_sort)
        i=0 
        ngrams = []
        for (k,v) in tmp[0:n]:
            ngrams.append((k,i))
            i += 1
        ngrams.sort()
        return ngrams

    def ngrams(self, text, n):
        """
            Interface for __get_ngrams, I dunno why I've done in this 
            way, but I did it ;)
        """
        return self.__get_ngrams(text, n)
