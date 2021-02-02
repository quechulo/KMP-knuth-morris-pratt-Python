""" KMP algorithm class

    Implementation of 'Knuth–Morris–Pratt' algorithm
    and function find() returning list of first indexes of
    pattern occurrence in the given string.
    Example of use:
                    kmp = KMP()
                    text = "abbbabababbaaaab"
                    pattern = "bba"
                    listOfIndexes = kmp.find( pattern, text )
    
"""


class KMP:
    dfa = {}

    def dfa_make(self, pat):
        pattern = pat
        txt = ""
        M = len(pat)
        ###############
        # making dfa using only alphabet from pattern
        for i in range(M):
            txt += pattern[i] + " @ []/ "
        txt = txt[0:(len(txt)-2)]

        # turning string into dictionary containing arrays
        self.dfa = dict((x.strip(), y.strip())
                        for x, y in (element.split('@')
                        for element in txt.split('/ ')))
        for i in range(M):
            self.dfa[pattern[i]] = [0]
            for _ in range(M - 1):
                self.dfa[pattern[i]].append(0)
        ###############
        R = len(self.dfa)  # len of alphabet

        self.dfa[pat[0]][0] = 1
        x = 0
        for j in range(1, M):
            for c in range(0, R):
                # coping of unmatched values
                self.dfa[pat[c]][j] = self.dfa[pat[c]][x]
            # set value for a match
            self.dfa[pat[j]][j] = j + 1
            # update value of restart
            x = self.dfa[pat[j]][x]

    def search(self, pat, text):
        N = len(text)
        M = len(pat)
        listOfIndex = []

        # flag for last occurence in pattern
        # of first letter in pattern
        flag = 0
        for i in range(1, M):
            if pat[M-i] == pat[0]:
                flag = M - i
                flag = M - flag
                break
        # saves ex. "aaa" "aa" => [0, 1]

        i = 0
        j = 0
        while(i < N):
            if text[i] in self.dfa:
                # using prepared dfa
                j = self.dfa[text[i]][j]
            else:
                # if some other character
                j = 0
            i += 1
            if j == M:
                listOfIndex.append(i - M)
                j = 0
                i -= flag

        return listOfIndex

    def find(self, pat, text):
        listOfIndex = []
        # if pattern is empty
        if len(pat) == 0:
            return listOfIndex
        self.dfa_make(pat)
        listOfIndex = self.search(pat, text)
        return listOfIndex
