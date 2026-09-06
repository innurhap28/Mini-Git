# Mini Git

Python으로 구현한 CLI 기반 Mini Git

Git의 핵심 구조인 **커밋 그래프, 브랜치, 커밋 탐색, 역색인, 정렬 알고리즘**을 직접 구현하여 Git의 내부 동작 원리를 이해하는 것을 목표로 합니다.

## 1. 프로젝트 소개

Mini Git은 실제 Git의 파일 추적이나 네트워크 기능을 구현하는 대신, 커밋의 메타데이터와 커밋 간 관계를 메모리에서 관리합니다.

주요 기능은 다음과 같습니다.

* 저장소 초기화
* 브랜치 생성 및 전환
* 커밋 생성
* 커밋 로그 출력
* 커밋 간 최단 경로 탐색
* 커밋의 조상 탐색
* 키워드 및 작성자 기반 검색
* 날짜 및 작성자 기준 로그 정렬
* CLI REPL 환경 제공

> 파일 내용 추적이나 실제 Git 저장소와의 연동은 구현하지 않습니다.

## 2. 실행 방법

Python 3 환경에서 실행합니다.

```bash
python3 main.py
```

실행하면 다음과 같은 CLI 환경이 시작됩니다.

```text
mini-git>
```

`exit` 또는 `quit`을 입력하면 프로그램을 종료할 수 있습니다.

## 3. 프로젝트 구조

```text
B3-2/
├── main.py
├── mini_git.py
├── repository.py
├── commit.py
├── branch.py
├── graph.py
├── search.py
├── sort.py
└── README.md
```

### 파일별 역할

| 파일              | 역할                                             |
| --------------- | ---------------------------------------------- |
| `main.py`       | CLI 진입점 및 명령어 파싱                               |
| `mini_git.py`   | Repository, Graph, Search, Sort를 연결하는 핵심 인터페이스 |
| `repository.py` | 커밋과 브랜치 저장 및 관리                                |
| `commit.py`     | Commit 객체 정의                                   |
| `branch.py`     | Branch 객체 정의                                   |
| `graph.py`      | 커밋 그래프 탐색, LOG, PATH, ANCESTORS                |
| `search.py`     | 키워드/작성자 역색인 관리                                 |
| `sort.py`       | 직접 구현한 정렬 알고리즘                                 |
| `README.md`     | 프로젝트 설명 및 사용 방법                                |

## 4. 주요 명령어

### 저장소 및 브랜치

| 명령어                    | 설명                              |
| ---------------------- | ------------------------------- |
| `INIT <user_name>`     | 저장소를 초기화하고 `main` 브랜치와 HEAD를 생성 |
| `BRANCH <branch_name>` | 현재 HEAD를 가리키는 새로운 브랜치 생성        |
| `SWITCH <branch_name>` | 지정한 브랜치로 HEAD 이동                |
| `COMMIT <message>`     | 현재 HEAD를 부모로 하는 새로운 커밋 생성       |

커밋 메시지나 사용자명 등에 공백이 포함되는 경우 따옴표를 사용할 수 있습니다.

```text
COMMIT "Add login feature"
```

### 로그 및 그래프 탐색

| 명령어                        | 설명                            |
| -------------------------- | ----------------------------- |
| `LOG`                      | 부모 커밋이 자식 커밋보다 먼저 출력되도록 로그 출력 |
| `PATH <commit1> <commit2>` | 두 커밋 사이의 최단 경로 탐색             |
| `ANCESTORS <commit_hash>`  | 특정 커밋에서 도달 가능한 모든 조상 커밋 탐색    |

`PATH`에서는 커밋과 부모의 연결을 **무방향 그래프의 간선**으로 취급합니다.

### 검색 및 정렬

| 명령어                      | 설명              |
| ------------------------ | --------------- |
| `SEARCH <keyword>`       | 커밋 메시지의 키워드로 검색 |
| `SEARCH --author=<name>` | 작성자로 커밋 검색      |
| `LOG --sort-by=date`     | 날짜 기준으로 로그 정렬   |
| `LOG --sort-by=author`   | 작성자 기준으로 로그 정렬  |

## 5. 커밋 구조

하나의 커밋은 다음 정보를 가지고 있습니다.

```text
Commit
├── hash
├── message
├── author
├── timestamp
└── parents
```

예를 들어:

```text
A
↓
B
↓
C
```

각 커밋은 자신의 부모 커밋을 `parents`에 저장합니다.

```text
A.parents = []
B.parents = [A]
C.parents = [B]
```

브랜치는 특정 커밋을 가리키는 포인터 역할을 하며, HEAD는 현재 브랜치를 가리킵니다.

```text
HEAD
 ↓
main
 ↓
Commit C
```

### DAG 구조

커밋은 일반적으로 이미 생성된 부모 커밋을 가리키며 새로운 커밋을 생성하는 방향으로 연결되기 때문에 **방향성 비순환 그래프(DAG)** 형태로 관리됩니다.

브랜치가 분기되면 다음과 같은 구조가 됩니다.

```text
        B ── C
       /
A ───
       \
        D ── E
```

이러한 구조를 이용하여 커밋 간의 관계를 탐색할 수 있습니다.

## 6. Repository

`Repository`는 Mini Git의 전체 상태를 관리합니다.

```python
self.commits = {}
self.branches = {}
self.head = None
self.current_user = None
```

### Commit 저장

커밋은 hash를 key로 사용하는 dictionary에 저장합니다.

```text
commits
├── "2fbabb" → Commit
├── "bac465" → Commit
└── "be4730" → Commit
```

따라서 commit hash를 이용하여 커밋을 빠르게 조회할 수 있습니다.

### Branch 관리

브랜치는 이름과 현재 가리키는 커밋 hash를 가지고 있습니다.

```text
branches
├── main    → be4730
└── feature → adc2b9
```

HEAD는 현재 브랜치 이름을 저장합니다.

```text
HEAD → main → be4730
```

## 7. 커밋 그래프 탐색

`graph.py`에서는 커밋 간 부모 관계를 이용하여 그래프 탐색 기능을 구현합니다.

### ANCESTORS

특정 커밋에서 부모를 따라가며 모든 조상 커밋을 탐색합니다.

DFS(깊이 우선 탐색)를 이용하여 부모 방향으로 재귀적으로 탐색합니다.

```text
C
↓
B
↓
A
```

`ANCESTORS C`를 실행하면 `B`, `A`를 찾을 수 있습니다.

### PATH

두 커밋 사이의 최단 경로를 찾기 위해 BFS(너비 우선 탐색)를 사용합니다.

커밋의 부모 관계를 다음과 같이 무방향 간선으로 취급합니다.

```text
A ─ B ─ C
    │
    D
```

따라서 부모 방향뿐만 아니라 자식 방향으로도 이동할 수 있습니다.

최단 경로가 존재하지 않는 경우 `No path`를 출력합니다.

## 8. LOG와 위상 정렬

일반적인 Git 로그와 달리 Mini Git의 `LOG`는 **부모 커밋이 자식 커밋보다 먼저 출력**되도록 구현합니다.

예를 들어:

```text
A
↓
B
↓
C
```

다음 순서로 출력됩니다.

```text
A
B
C
```

이를 위해 커밋 간의 부모-자식 관계를 이용하여 위상 정렬과 유사한 방식으로 출력 순서를 구성합니다.

## 9. 역색인(Inverted Index)

커밋 검색에서는 모든 커밋을 하나씩 순회하는 대신 **역색인**을 사용합니다.

`search.py`에서는 두 종류의 인덱스를 관리합니다.

```text
keyword_index
keyword → commit_hash 목록

author_index
author → commit_hash 목록
```

예를 들어 다음과 같은 커밋이 존재한다면:

```text
A: Initial commit
B: Add login feature
C: Fix login bug
```

키워드 `login`은 다음과 같이 관리할 수 있습니다.

```text
login → [B, C]
```

따라서 `SEARCH login`을 수행하면 모든 커밋을 순회하지 않고 `login`에 해당하는 커밋 hash 목록을 먼저 가져올 수 있습니다.

### 키워드 정규화

커밋 메시지를 공백 기준으로 분리하고 소문자로 변환하여 키워드를 저장합니다.

```text
"Add Login Feature"
```

↓

```text
add
login
feature
```

## 10. 정렬 알고리즘

Python의 기본 정렬 API인 다음 함수는 사용하지 않습니다.

```python
sorted()
list.sort()
```

대신 `sort.py`에서 정렬 알고리즘을 직접 구현합니다.

현재는 **Insertion Sort**를 사용하며, 비교 기준을 함수로 전달하여 정렬 기준을 변경할 수 있도록 구현했습니다.

```text
LOG --sort-by=date
```

에서는 timestamp를 기준으로 정렬하고,

```text
LOG --sort-by=author
```

에서는 author를 기준으로 정렬합니다.

### Insertion Sort

Insertion Sort의 기본적인 동작은 다음과 같습니다.

```text
정렬된 영역에 새로운 값을 하나씩 삽입
↓
앞의 값과 비교
↓
필요하면 값을 이동
↓
모든 값이 정렬될 때까지 반복
```

시간 복잡도는 다음과 같습니다.

| 경우 | 시간 복잡도 |
| -- | ------ |
| 평균 | O(n²)  |
| 최악 | O(n²)  |
| 최선 | O(n)   |

Insertion Sort는 같은 값의 상대적인 순서를 유지할 수 있는 **안정 정렬(Stable Sort)**입니다.

## 11. 사용한 주요 알고리즘 및 자료구조

| 기능        | 자료구조 / 알고리즘            |
| --------- | ---------------------- |
| Commit 저장 | Dictionary             |
| Branch 관리 | Dictionary + Branch 객체 |
| 커밋 그래프    | Commit의 `parents` 관계   |
| ANCESTORS | DFS                    |
| PATH      | BFS                    |
| LOG       | 위상 정렬 성격의 탐색           |
| SEARCH    | Inverted Index         |
| LOG 정렬    | Insertion Sort         |

## 12. 설계 구조

전체적인 데이터 흐름은 다음과 같습니다.

```text
                 ┌─────────────┐
                 │   main.py   │
                 │     CLI     │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  MiniGit    │
                 └──────┬──────┘
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 ┌────────────┐  ┌────────────┐  ┌────────────┐
 │ Repository │  │   Graph    │  │   Search   │
 └─────┬──────┘  └────────────┘  └────────────┘
       │
       ▼
 ┌────────────┐
 │   Commit   │
 └────────────┘

                 ┌────────────┐
                 │    Sort    │
                 └────────────┘
```

각 기능을 별도의 클래스와 파일로 분리하여 CLI, 저장소 관리, 그래프 탐색, 검색, 정렬의 역할을 구분했습니다.

## 13. 구현 범위 및 제한사항

본 프로젝트에서는 학습 목적에 맞게 다음 범위만 구현합니다.

* 커밋 메타데이터 관리
* 브랜치 관리
* 커밋 그래프 탐색
* 검색 및 정렬
* CLI 기반 REPL

다음 기능은 구현하지 않습니다.

* 실제 파일 변경 내용 추적
* 네트워크 통신
* 파일 기반 데이터 영속성
* 그래프 전용 라이브러리 사용

데이터는 프로그램 실행 중 메모리에 저장되며, 프로그램 종료 시 초기화됩니다.

## 14. 학습 목표

이 프로젝트를 통해 다음 개념을 직접 구현하고 이해하는 것을 목표로 했습니다.

* Git 커밋과 브랜치의 관계
* DAG와 그래프 탐색
* BFS / DFS
* 위상 정렬
* 해시 기반 빠른 조회
* 역색인의 동작 원리
* 정렬 알고리즘의 직접 구현
* 알고리즘의 시간 복잡도
* CLI 프로그램의 명령어 파싱 및 실행 구조
