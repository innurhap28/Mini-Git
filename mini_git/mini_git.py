# CLI 명령을 실제 기능과 연결

from repository import Repository
from graph import Graph
from sort import Sort

class MiniGit:
    def __init__(self):
        self.repository = Repository()
        self.graph = Graph(self.repository)
        self.sort = Sort()

    def init(self, user_name):
        self.repository.init_repository(user_name)

    def branch(self, branch_name):
        self.repository.create_branch(branch_name)

    def switch(self, branch_name):
        self.repository.switch_branch(branch_name)

    def commit (self, message):
        return self.repository.create_commit(message)

    def log(self):
        return self.graph.log()

    def ancestors(self, commit_hash):
        return self.graph.ancestors(commit_hash)

    def path(self, commit1, commit2):
        return self.graph.path(commit1, commit2)

    def search(self, keyword=None, author=None):
        if author is not None:
            hashes = self.repository.search.search_author(author)
        else:
            hashes = self.repository.search.search_keyword(keyword)

        commits = []
        for commit_hash in hashes:
            commits.append(self.repository.get_commit(commit_hash))
        return commits

    def log_sorted(self, sort_by):
        commits = self.graph.log()
        if sort_by == "date":
            return self.sort.insertion_sort(commits, lambda commit: commit.timestamp)
        if sort_by == "author":
            return self.sort.insertion_sort(commits, lambda commit: commit.author)

        raise ValueError("Invalid sort option")
        