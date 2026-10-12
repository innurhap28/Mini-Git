# keyword/author 역색인

class Search:
    def __init__(self):
        self.keyword_index = {}
        self.author_index = {}

    def add_commit(self, commit):
        # author -> commit hash
        author = commit.author

        if author not in self.author_index:
            self.author_index[author] = []

        self.author_index[author].append(commit.hash)

        # keyword -> commit hahs
        keywords = commit.message.split()

        for keyword in keywords:
            keyword = keyword.lower()
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = []

            if commit.hash not in self.keyword_index[keyword]:
                self.keyword_index[keyword].append(commit.hash)

    def search_keyword(self, keyword):
        keyword = keyword.lower()
        return self.keyword_index.get(keyword, [])

    def search_author(self, author):
        return self.author_index.get(author, [])