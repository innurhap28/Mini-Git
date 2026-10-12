# 커밋 그래프 탐색, PATH, ANCESTORS, LOG

from sort import Sort

class Graph:
    def __init__(self, repository):
        self.repository = repository
        self.sorter = Sort()

    def _dfs(self,start_hash, get_neighbors_fn, visited=None):
        """
        공통 DFS 순회 유틸
        - 반환 순서: 전위 순회(Pre-order) 방식에 따라 노드가 발견된 순서대로 반환
        """
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
        """
        공통 BFS 최단 경로 탐색 유틸
        - 동률 처리: get_neighbors_fn에서 이웃을 사전순 정렬하므로, 
          경로 길이가 같을 경우 해시 문자열 사전순으로 앞서는 경로를 먼저 선택
        """
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
        """
        공통 위상 정렬 유틸 (Kahn's Algorithm)
        - 반환 순서: 부모 노드가 자식 노드보다 먼저 오도록 정렬된 해시 리스트 반환
        """
        commits = list(self.repository.commits.values())
        parent_count = {commit.hash: len(commit.parents) for commit in commits}

        # 동일 진입차수(indegree == 0) 발생 시, 
        # repository.commits의 순회 순서(커밋 생성 순서)를 Tie-break 기준으로 사용.
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
        """
        커밋의 모든 조상 커밋을 반환
        - 반환값: 발견 순서(DFS)대로 정렬된 조상 커밋 객체 리스트
        - 예외 처리: 존재하지 않는 해시일 경우 repository.get_commit()에서 예외를 raise
        """
        self.repository.get_commit(commit_hash)
        parent_hashes = self._dfs(commit_hash, self._get_parents)
        return [self.repository.get_commit(h) for h in parent_hashes]

    def path(self, start_hash, target_hash):
        """
        두 커밋 사이의 무방향 최단 경로를 반환
        - 반환값: start_hash부터 target_hash까지의 최단 경로 커밋 해시 리시트 (경로 없을 시 None)
        """
        self.repository.get_commit(start_hash)
        self.repository.get_commit(target_hash)
        return self._bfs_path(start_hash, target_hash, self._get_neighbors)

    def log(self):
        """
        부모 커밋이 먼저 나오도록 커밋 로그를 반환
        - 반환값: 위상 정렬된 전체 커밋 객체 리스트
        """
        ordered_hashes = self._topological_sort()
        return [self.repository.get_commit(h) for h in ordered_hashes]