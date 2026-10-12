# 브랜치 생성/전환 관리

class Branch:
    def __init__(self, name, commit_hash=None):
        self.name = name
        self.commit_hash = commit_hash