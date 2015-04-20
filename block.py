words = ["doggy", "kitty"]

def block (sentence) :
    """removes bad words from sentence,
    returns the sanitized sentence"""
        
    for word in words:
        if word in sentence:
             return "[content inapropriate]"
    return sentence
if __name__ == "__main__":
    while True:
        print(block(raw_input()))
