


class NGram(object):
    def __init__(self, text, n=3):
        self.length = None
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.calculate_length()
 
    def parse_text(self, text):
        chars = ' ' * self.n 
        # initial sequence of spaces with length n
        for letter in (" ".join(text.split()) + " "):
            chars = chars[1:] + letter 
            # append letter to sequence of length n
            self.table[chars] = self.table.get(chars, 0) + 1 
            # increment count
        
    # """ Treat the N-Gram table as a vector and return its scalar magnitudeto be used for performing a vector-based search.""" 
    def calculate_length(self):
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length

    # """ Find the difference between two NGram objects by finding the cosine of the angle between the two vector representations of the table of
    # N-Grams. Return a float value between 0 and 1 where 0 indicates that the two NGrams are exactly the same."""
    def __sub__(self, other):
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")
 
        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")
 
        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)
 
        return 1.0 - (float(total) )/ (float(self.length) * float(other.length))
 
    # """ Out of a list of NGrams that represent individual languages, return the best match."""
    def find_match(self, languages):
        return min(languages, lambda n: self - n)
if __name__ == '__main__':
    trigram = NGram('calculates the scalar length of the trigram vector and stores it in self.length',3);