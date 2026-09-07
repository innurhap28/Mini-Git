# 커밋 그래프 탐색, PATH, ANCESTORS, LOG

from sort import Sort

class Graph:
    def __init__(self, repository):
        self.repository = repository
        self.sorter = Sort()

# ------------------------
# ANCESTORS
# ------------------------


    def _dfs(self,start_hash, get_neighbors_fn, visited=None):
        """공통 DFS 순회 유틸"""
        if visited is None:
            visited = set()
        visited.add(start_hash)
        nodes = []

        for neighbor in get_neighbors_fn(start_hash):
            if neighbor not in visited:
                nodes.append(neighbor)
                nodes.extend(self._dfs(neighbor, get_neighbors_fn, visited))

        return nodes

    def _bfs_path(self, start_hash, target_hash, get_neighbors_fn):
        """공통 BFS 최단 경로 탐색 유틸"""
        if start_hash == target_hash:
            return [start_hash]

        queue = [[start_hash]]
        visited = {start_hash}

        while queue:
            current_path = queue.pop(0)
            current_hash = current_path[-1]

            for neighbor_hash in get_neighbors_fn(current_hash):
                if neighbor_hash in visited:
                    continue
                new_path = current_path + [neighbor_hash]
                if neighbor_hash == target_hash:
                    return new_path

                visited.add(neighbor_hash)
                queue.append(new_path)
        return None

    def _topological_sort(self):
        """공통 위상 정렬 유틸 (Kahn's Algorithm)"""
        commits = list(self.repository.commits.values())
        parent_count = {commit.hash: len(commit.parents) for commit in commits}

        queue = [commit.hash for commit in commits if parent_count[commit.hash] == 0]
        result_hashes = []

        while queue:
            current_hash = queue.pop(0)
            result_hashes.append(current_hash)

            for child_hash, child_commit in self.repository.commits.items():
                if current_hash in child_commit.parents:
                    parent_count[child_hash] -= 1
                    if parent_count[child_hash] == 0 and child_hash not in queue:
                        queue.append(child_hash)

        return result_hashes
    
    def _get_parents(self, commit_hash):
        """부모 노드 탐색 헬퍼"""
        commit = self.repository.get_commit(commit_hash)
        return commit.parents

    def _get_neighbors(self, commit_hash):
        """부모 및 자식 노드 탐색 헬퍼 (정렬 포함)"""
        raw_neighbors = []
        commit = self.repository.get_commit(commit_hash)

        # 부모 노드 수집 (중복 제외)
        for parent_hash in commit.parents:
            if parent_hash not in raw_neighbors:
                raw_neighbors.append(parent_hash)

        # 자식 노드 수집 (중복 제외)
        for other_hash, other_commit in self.repository.commits.items():
            if commit_hash in other_commit.parents:
                if other_hash not in raw_neighbors:
                    raw_neighbors.append(other_hash)

        neighbors = self.sorter.insertion_sort(raw_neighbors, key=lambda x: x)
        return neighbors

# ========================
# Public methods .. 
# ========================

    def ancestors(self, commit_hash):
        """커밋의 모든 조상 커밋을 반환"""
        self.repository.get_commit(commit_hash)
        parent_hashes = self._dfs(commit_hash, self._get_parents)
        return [self.repository.get_commit(h) for h in parent_hashes]

    def path(self, start_hash, target_hash):
        """두 커밋 사이의 무방향 최단 경로를 반환"""
        self.repository.get_commit(start_hash)
        self.repository.get_commit(target_hash)
        return self._bfs_path(start_hash, target_hash, self._get_neighbors)

    def log(self):
        """부모 커밋이 먼저 나오도록 커밋 로그를 반환"""
        ordered_hashes = self._topological_sort()
        return [self.repository.get_commit(h) for h in ordered_hashes]