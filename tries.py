class triNode:
    def __init__(self, letter, unique):
        self.letter = letter
        self.neighbors = dict()
        self.uniqueLetters = unique
        self.isWord = False

class tri:
    def __init__(self, start):
        self.doNotUse = set()
        self.head = triNode("", 0)
        self.notAtLevel = dict()
        self.atLevel = dict()
        self.notCorrect = set()
        self.notLocated = set()
        self.first = True
        self.levelArray = ["*", "*", "*", "*" ,"*", "*"]
        self.startWord = start
        for i in range(7):
            self.notAtLevel[i] = set()
            self.atLevel[i] = set()

    def recursiveInsert(self, cur, word, level, num):
        if word == "":
            cur.isWord = True
            return
        if word[0] not in cur.neighbors:
            newNode = triNode(word[0], num)
            cur.neighbors[word[0]] = newNode
        self.recursiveInsert(cur.neighbors[word[0]], word[1:], level+1, num)

    def insert(self, word, bias):
        letters = set()
        for c in word:
            letters.add(c)
        self.recursiveInsert(self.head, word, 0, len(letters) + bias)


    def recursiveSearch(self, cur, word):
        if word == "":
            return cur.isWord

        if word[0] not in cur.neighbors:
            return False

        return self.recursiveSearch(cur.neighbors[word[0]], word[1:])
        
    def search(self, word):
        return self.recursiveSearch(self.head, word)


    def recursiveFind(self, cur, level, word, lettersNeeded):
        if self.first:
            self.first = False
            return [True, self.startWord , 0]
        if cur.isWord:
            if (len(lettersNeeded) == 0) and word not in self.doNotUse:
                return [True, word, cur.uniqueLetters]
            return [False, "ERROR", 0]

        sol = [False, "ERROR", 0]
        maxUnique = 0
        for i in cur.neighbors:
            trysol = [False, "errOR", 0]
            if self.levelArray[level] == "*":
                if i in self.notAtLevel[level] or i in self.notCorrect:
                    continue
                restore = lettersNeeded.copy()
                if i in lettersNeeded:
                    lettersNeeded.remove(i)
                trysol = self.recursiveFind(cur.neighbors[i], level+1, word + i, lettersNeeded)
                lettersNeeded = restore
            else:
                if i != self.levelArray[level]:
                    continue
                trysol = self.recursiveFind(cur.neighbors[i], level+1, word + i, lettersNeeded)

            if sol[2] < trysol[2]:
                sol = trysol
        return sol

    def findAWord(self):
        word =  self.recursiveFind(self.head, 0, "", self.notLocated)[1]
        #print("try " + word)
        self.notLocated = set()        
        for level, c in enumerate(word):

            val = input("is " + c + " in the right place?")
            if self.levelArray[level] != "*":
                val = "d"
            

            if val == "d":
                self.levelArray[level] = c
            elif val == "a":
                if c not in self.notLocated:
                    self.notCorrect.add(c)
            elif val == "x":
                return True
            elif val == "s":
                self.doNotUse.add(word)
                return False
            elif val == "q":
                self.doNotUse = set()
                self.notAtLevel = dict()
                self.atLevel = dict()
                self.notCorrect = set()
                self.notLocated = set()
                self.first = True
                self.levelArray = ["*", "*", "*", "*" ,"*", "*"]
                for i in range(7):
                    self.notAtLevel[i] = set()
                    self.atLevel[i] = set()
                return False
            else:
                self.notAtLevel[level].add(c)
                self.notLocated.add(c)
        return False

    def findAWordNoInput(self, word, arr):
        #print(word)
        #print(arr)
        self.notLocated = set()   
        for level, c in enumerate(word):
            val = arr[level]         
            if val == "G" or val == 'g':
                self.levelArray[level] = c
                #print(val, "G")
            elif val == "B" or val == 'b':
                if c not in self.notLocated:
                    self.notCorrect.add(c)
                #print(val, "B")
            elif val == "s":
                self.doNotUse.add(word)
                return False
            elif val == "q":
                self.doNotUse = set()
                self.notAtLevel = dict()
                self.atLevel = dict()
                self.notCorrect = set()
                self.notLocated = set()
                self.first = True
                self.levelArray = ["*", "*", "*", "*" ,"*", "*"]
                for i in range(7):
                    self.notAtLevel[i] = set()
                    self.atLevel[i] = set()
                return False
            else:
                self.notAtLevel[level].add(c)
                self.notLocated.add(c)
                #print(val, "Y")
        return False