# Commit 객체 정의

class Commit:
    def __init__(self, commit_hash, message, author, timestamp, parents, branch):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = parents
        self.branch = branch