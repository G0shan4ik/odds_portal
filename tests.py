import Levenshtein

def jaccard_similarity(str1: str, str2: str) -> float:
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def levenshtein_similarity(str1: str, str2: str) -> float:
    distance = Levenshtein.distance(str1, str2)

    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    return (max_len - distance) / max_len


d = 'ситл маринерс – го уайт чика сокс'

def check_command(str1: str, str2: str) -> bool:
    str1, str2 = str1.lower(), str2.lower()
    print(str1, str2)
    return True if (
            float(f"{levenshtein_similarity(str1, str2):.2f}") >= 0.67 or
            float(f"{jaccard_similarity(str1, str2):.2f}") >= 0.5
    ) else False



