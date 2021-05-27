from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.pd = []
        self.dictionary = dict()

    def fit(self, X, y, d):
        # Fit Naive Bayes classifier according to X, y. 
        self.pd = [0] * len(d)
        for i in range(len(y)):
            w = X[i].split()
            self.pd[d[y[i]]] += 1
            for j in w:
                if j not in self.dictionary:
                    self.dictionary[j] = [0] * (2 * len(d) + 1)
                self.dictionary[j][d[y[i]]] += 1
                self.dictionary[j][2 * len(d)] += 1
        nt = [0] * len(d)
        for i in self.dictionary.keys():
            for j in range(len(d)):
                nt[j] += self.dictionary[i][j]
        for i in self.dictionary.keys():
            for j in range(len(d)):
                self.dictionary[i][len(d) + j] = (self.dictionary[i][j] + self.alpha) / (
                        self.dictionary[i][2 * len(d)] + self.alpha * len(self.dictionary))

    def predict(self, X):
        #Perform classification on an array of test vectors X.
        arr = []
        for i in range(len(X)):
            w = X[i].split()
            pb = [log(i) for i in self.pd]
            for j in w:
                for k in range(len(self.pd)):
                    if j not in self.dictionary:
                        continue
                    pb[k] += log(self.dictionary[j][len(self.pd) + k])
            mn = 0
            mx = pb[0]
            for j in range(1, len(self.pd)):
                if pb[j] > mx:
                    mx = pb[j]
                    mn = j
                    print(X[i], pb)
            arr.append(mn)
        return arr

    def score(self, label_mes1, label_mes2, d):
        # Returns the mean accuracy on the given test data and labels.
        count = 0
        arr = [d[i] for i in label_mes2]
        a = self.predict(label_mes1)
        for i in range(len(label_mes2)):
            if a[i] == arr[i]:
                count += 1
        return count / len(label_mes2)


# Checking

mes1 = [
    "i love this sandwich",
    "this is an amazing place",
    "i feel very good about these beers",
    "this is my best work",
    "what an awesome view",
    "i do not like this restaurant",
    "i am tired of this stuff",
    "i cant deal with this",
    "he is my sworn enemy",
    "my boss is horrible",
]

label_mes1 = [
    "the beer was good",
    "i do not enjoy my job",
    "i aint feeling dandy today",
    "i feel amazing",
    "gary is a friend of mine",
    "i cant believe im doing this",
]

mes2 = [
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
]

label_mes2 = [
    "Positive",
    "Negative",
    "Negative",
    "Positive",
    "Positive",
    "Negative"
]

d = {"Positive": 0, "Negative": 1}
test = NaiveBayesClassifier(0.1)
test.fit(mes1, mes2, d)
print(test.score(label_mes1, label_mes2, d))
