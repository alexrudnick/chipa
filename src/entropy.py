import math
 
def entropy(things):
    terms = []
    for thingtype in set(things):
        prob = things.count(thingtype) / len(things)
        terms.append(prob * math.log(prob, 2))
    return (-1) * sum(terms)

if __name__ == "__main__":
    print(entropy("this should print two".split()))
