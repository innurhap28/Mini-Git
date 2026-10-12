# Mini Git CLI 테스트

## 1. 기본 초기화 및 커밋 테스트

```text
mini-git> INIT Alice
mini-git> COMMIT "Initial commit"
mini-git> COMMIT "Add login feature"
mini-git> COMMIT "Fix login bug"
```

### 확인 사항

* `INIT` 실행 시 저장소가 초기화되는가?
* 현재 사용자가 `Alice`로 설정되는가?
* `COMMIT`마다 서로 다른 commit hash가 생성되는가?
* 두 번째 커밋부터 이전 커밋이 `parent`로 연결되는가?

예상 그래프:

```text
Initial commit
      ↓
Add login feature
      ↓
Fix login bug
```

---

## 2. LOG 테스트

```text
mini-git> LOG
```

### 확인 사항

부모 커밋이 자식 커밋보다 먼저 출력되어야 한다.

예:

```text
xxxxxx Alice 2026-09-07 00:00:00 Initial commit
xxxxxx Alice 2026-09-07 00:00:01 Add login feature
xxxxxx Alice 2026-09-07 00:00:02 Fix login bug
```

> commit hash와 timestamp는 실제 실행 결과에 따라 달라진다.

---

## 3. Branch 테스트

현재 `Fix login bug`까지 커밋된 상태에서:

```text
mini-git> BRANCH feature
mini-git> SWITCH feature
mini-git> COMMIT "Add payment feature"
```

다시 main으로 이동:

```text
mini-git> SWITCH main
mini-git> COMMIT "Update README"
```

### 예상 그래프

```text
                 ┌── Add payment feature
                 │
Initial → Login → Fix login bug
                 │
                 └── Update README
```

### 확인 사항

* `BRANCH feature`가 현재 HEAD를 가리키는가?
* `SWITCH feature` 이후 커밋이 feature 브랜치에 추가되는가?
* `SWITCH main` 이후 커밋이 main 브랜치에 추가되는가?
* 두 브랜치가 같은 커밋에서 갈라지는가?

---

# 4. ANCESTORS 테스트

`Fix login bug`의 hash를 확인한 후:

```text
mini-git> ANCESTORS <Fix-login-bug-hash>
```

예:

```text
mini-git> ANCESTORS 6479e1
```

### 확인 사항

해당 커밋 자신은 출력하지 않고 부모와 그 조상만 출력되어야 한다.

예:

```text
b80aaa
123456
```

---

# 5. PATH 테스트

커밋 hash를 각각 확인한 후 두 커밋 사이의 경로를 테스트한다.

```text
mini-git> PATH <commit1> <commit2>
```

예:

```text
mini-git> PATH 123456 6479e1
```

예상:

```text
123456->b80aaa->6479e1
```

### 반대 방향도 테스트

```text
mini-git> PATH 6479e1 123456
```

예상:

```text
6479e1->b80aaa->123456
```

### 존재하지 않는 경로 테스트

서로 연결되지 않은 커밋이 있는 경우:

```text
mini-git> PATH <commit1> <commit2>
```

예상:

```text
No path
```

### 같은 커밋 테스트

```text
mini-git> PATH 6479e1 6479e1
```

예상:

```text
6479e1
```

---

# 6. SEARCH 키워드 테스트

다음과 같은 커밋이 있다고 가정한다.

```text
Initial commit
Add login feature
Fix login bug
Add payment feature
```

검색:

```text
mini-git> SEARCH login
```

`login`이 포함된 커밋만 출력되어야 한다.

```text
xxxxxx Alice ... Add login feature
xxxxxx Alice ... Fix login bug
```

### 대소문자 테스트

```text
mini-git> SEARCH LOGIN
```

```text
mini-git> SEARCH Login
```

```text
mini-git> SEARCH login
```

세 검색 결과가 동일해야 한다.

---

# 7. SEARCH 작성자 테스트

```text
mini-git> SEARCH --author=Alice
```

확인 사항:

* Alice가 작성한 커밋만 출력되는가?
* 작성자 역색인을 사용하는가?

다른 사용자의 커밋을 만들 수 있도록 현재 구조에서 사용자를 변경하는 기능이 있다면 추가로 테스트한다.

---

# 8. 존재하지 않는 검색어 테스트

```text
mini-git> SEARCH database
```

검색 결과가 없다면 오류 없이 빈 결과가 출력되어야 한다.

---

# 9. LOG 날짜 정렬 테스트

```text
mini-git> LOG --sort-by=date
```

확인 사항:

* 날짜/시간을 기준으로 정렬되는가?
* `sorted()` 또는 `.sort()`를 사용하지 않았는가?

---

# 10. LOG 작성자 정렬 테스트

```text
mini-git> LOG --sort-by=author
```

확인 사항:

* 작성자 이름을 기준으로 정렬되는가?
* 직접 구현한 정렬 알고리즘을 사용하는가?

---

# 11. 잘못된 명령어 테스트

```text
mini-git> HELLO
```

예상:

```text
Unknown command
```

---

# 12. 잘못된 인자 개수 테스트

```text
mini-git> INIT
```

```text
mini-git> BRANCH
```

```text
mini-git> SWITCH
```

```text
mini-git> COMMIT
```

```text
mini-git> PATH
```

예상:

```text
Invalid args
```

---

# 13. 존재하지 않는 Branch 테스트

```text
mini-git> SWITCH develop
```

존재하지 않는 브랜치라면 오류 메시지가 출력되어야 한다.

---

# 14. 존재하지 않는 Commit 테스트

```text
mini-git> ANCESTORS abc123
```

```text
mini-git> PATH abc123 def456
```

존재하지 않는 commit hash를 입력했을 때 적절한 오류 메시지가 출력되어야 한다.

---

# 15. 종료 테스트

```text
mini-git> exit
```

또는:

```text
mini-git> quit
```

프로그램이 정상적으로 종료되어야 한다.

대소문자도 확인한다.

```text
mini-git> EXIT
```

```text
mini-git> QUIT
```

---

# 16. KeyboardInterrupt / EOF 테스트

프로그램 실행 중:

```text
mini-git> 
```

상태에서 `Ctrl + C`를 입력한다.

또는 `Ctrl + D`를 입력한다.

프로그램이 traceback 없이 정상적으로 종료되는지 확인한다.

---

# 17. 전체 통합 테스트

처음부터 새로 실행하여 다음 순서로 테스트한다.

```text
mini-git> INIT Alice

mini-git> COMMIT "Initial commit"

mini-git> COMMIT "Add login feature"

mini-git> COMMIT "Fix login bug"

mini-git> BRANCH feature

mini-git> SWITCH feature

mini-git> COMMIT "Add payment feature"

mini-git> SWITCH main

mini-git> COMMIT "Update README"

mini-git> LOG

mini-git> LOG --sort-by=date

mini-git> LOG --sort-by=author

mini-git> SEARCH login

mini-git> SEARCH --author=Alice
```

이후 각 commit hash를 이용하여:

```text
mini-git> ANCESTORS <commit_hash>

mini-git> PATH <commit_hash1> <commit_hash2>
```

를 테스트한다.

---

## 테스트 체크리스트

* [ ] INIT
* [ ] COMMIT
* [ ] BRANCH
* [ ] SWITCH
* [ ] LOG
* [ ] LOG --sort-by=date
* [ ] LOG --sort-by=author
* [ ] ANCESTORS
* [ ] PATH
* [ ] SEARCH
* [ ] SEARCH --author
* [ ] 대소문자 무시
* [ ] 따옴표를 사용한 공백 포함 메시지
* [ ] 잘못된 명령어
* [ ] 잘못된 인자
* [ ] 존재하지 않는 Branch
* [ ] 존재하지 않는 Commit
* [ ] exit / quit
* [ ] Ctrl+C
* [ ] Ctrl+D
