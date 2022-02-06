def GreedyMotifSearchWithPseudocounts(Dna,k,t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
    n = len(Dna[0])
    for m in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][m:m+k])
        for j in range(1, t):
            P = ProfileWithPseudocounts(Motifs[0:j])
            Motifs.append(ProfileMostProbablePattern(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs
       
                    
import random

def RepeatedRandomizedMotifSearch(Dna,k,t,N):
    BestScore = float('inf')
    BestMotifs = []
    for i in range(N):
        Motifs = RandomizedMotifSearch(Dna, k, t)
        CurrScore = Score(Motifs)
        if CurrScore < BestScore:
            BestScore = CurrScore
            BestMotifs = Motifs
    return BestMotifs



# Input:  Positive integers k and t, followed by a list of strings Dna
# Output: RandomizedMotifSearch(Dna, k, t)
def RandomizedMotifSearch(Dna, k, t):
    # insert your code here
    M = RandomMotifs(Dna, k, t)
    BestMotifs = M    
    
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs 

# Insert necessary subroutines here, including RandomMotifs(), ProfileWithPseudocounts(), Motifs(), Score(),


def RandomMotifs(Dna, k, t):
    result = []
    for i in range(0,t):
        random_k = random.randint(0, len(Dna[i]) - k - 1)
        result.append(Dna[i][random_k: random_k + k])

    return result

# Input:  A profile matrix Profile and a list of strings Dna
# Output: Motifs(Profile, Dna)
def Motifs(Profile, Dna):
    # insert your code here
    return [ProfileMostProbablePattern(s, len(Profile['A']), Profile) for s in Dna]
        
  
def ProfileWithPseudocounts(Motifs):
    profile = {}
    k = len(Motifs[0])
    t = len(Motifs)
    profile = CountWithPseudocounts(Motifs)
    
    for i in range(k):
        p = 0
        
        for symbol in "ACGT":
            p = p+profile[symbol][i]
        for symbol in "ACGT":
            profile[symbol][i] = profile[symbol][i]/p
    return profile

def Score(Motifs):
    consensus = Consensus(Motifs)
    count = CountWithPseudocounts(Motifs)
    
    k = len(Motifs[0])
    t = len(Motifs)  
    c = 0
    for Motif in Motifs:
        for i in range(k):
                if Motif[i] != consensus[i]:
                    c = c+1
    return c


def Consensus(Motifs):
    consensus = ""
    k = len(Motifs[0])
    t = len(Motifs)
    count = CountWithPseudocounts(Motifs)
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

def CountWithPseudocounts(Motifs):
    count = {}
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(1)
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] = count[symbol][j]+1
    return count

def ProfileMostProbablePattern(Text, k, profile):
    n = len(Text)
    m = -1 
    x = Text[1:k]
    for i in range(n-k+1):
        Pattern =  Text[i:i+k]
        p = Pr(Pattern, profile)
        if p>m:
            m = p
            x = Pattern
            
    return x


def Pr(Text, Profile):
   
    p = 1
    for i in range(len(Text)):
        
        p1 = Profile[(Text[i])][i]
        p = p*p1
        
    return p
