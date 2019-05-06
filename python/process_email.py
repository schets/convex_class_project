import re
__email_regexes = [
    ('From .*Subject:', ''), #strips non-subject header
    ('Content-Type:[^\n]*', ''), #strips post-subject header
    ('X-Keywords:[^\n]*', ''), #strips post-subject header
    ('Content-Transfer-Encoding:[^\n]*', ''), #strips post-subject header
    ('<[^<>]+>', ' '), #strips html
    ('[0-9]+', 'number'), #replaces numbers
    ('(http|https)://[^\s]*', 'httpaddr'), #replace urls with httpaddr
    ('[^\s]+@[^\s]+', 'emailaddr'), #replace emails with emailaddr
    ('[$]+', 'dollar'), #replace dollar signs
    ('[@/#.-:&\*+=>_<;%]', ' '), #replace splitting punctuation with whitespace
    ('[^a-zA-Z0-9\s]|', '') #replace remaining punctuation with nothing
]

__email_regexes = [(re.compile(regex, re.DOTALL), rep)
                   for regex, rep in __email_regexes]

# stop word set used by nltk
# included directly to avoid runtime dependency
__stop_words = set(['ain', 'as', 'then', 's', 'yours', 'into', 'yourselves', 'his', 'its', 'from', 'been', 'during', "youll", "didnt", 'theirs', 'having', 'over', 'herself', 'further', 'those', 'now', 'am', "thatll", 're', "shes", 'were', 'itself', "arent", 'she', 'him', 'so', 'haven', "youd", "isnt", 'why', 'against', 'shouldn', 'have', 'whom', 'before', 'shan', "youre", 'do', 'm', 'mightn', 've', 'with', 'when', 'too', 'until', 'ourselves', 'are', 'i', 'who', "mustnt", "doesnt", 'how','himself', 'that', 'aren', 'my', 'more', "youve", 'where', 'y', 'didn', 'or', 'a', 'is', 'ours', 'he', 'off', 'doing', 'can', 'their', "wasnt", 'on', 'hers', 'same', 'has', 'of', 'being', 'some', 'doesn', 'mustn', "shouldve", 'll', 'will', 'other', "havent", 'was', 'hasn', 'up', 'but', 'by', 'down', 'you', "wouldnt", 'all', 'few', 'there', 'both', 'each', 'very', 'hadn', "hadnt", 'weren', 'isn', 'did', 'does', 'themselves', "dont", "werent", 'for', 'such', 'me', 'we', 'at', 'above', 'not', 'because', 'them', 'in', 'under', 'once', 'than', 'just', 'only', 'the', 'again', "couldnt", 'nor', 'her', 't', 'myself', 'which', 'don', 'd', "shouldnt", 'had', 'o', "neednt", 'any', 'and', "shant", 'if', 'while', 'ma', 'be', 'needn', 'yourself', 'won', 'your', "mightnt", 'these', 'between', 'here', 'they', "its", "wont", 'about', 'after', 'through', 'most', 'what', 'couldn', 'wouldn', 'to', 'our', 'an', 'below', 'out', 'own', 'wasn', 'should', "hasnt", 'it', 'this', 'no'])

def process_email(email):
    for regex, rep in __email_regexes:
        email = re.sub(regex, rep, email)
    email = email.lower()
    words = email.split()
    return [word for word in words if len(word) > 0 and word not in __stop_words]

if __name__ == '__main__':
    import argparse
    import stemmer

    parser = argparse.ArgumentParser(description='Load and clean email')
    parser.add_argument("--file", help="File to read the email from", required=True)
    parser.add_argument("--stem", action="store_true", help="Stem the parsed email")

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()
        words = process_email(content)
        if args.stem:
            words = [stemmer.stem(word) for word in words]
        print(" ".join(words))
