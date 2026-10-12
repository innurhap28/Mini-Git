# 직접 구현한 정렬 알고리즘

class Sort:
    def insertion_sort(self, commits, key):
        result = []

        for commit in commits:
            result.append(commit)

            i = len(result) - 1

            while i > 0:
                current = result[i]
                previous = result[i - 1]

                if key(current) >= key(previous):
                    break

                result[i] = previous
                result[i - 1] = current

                i -= 1

        return result