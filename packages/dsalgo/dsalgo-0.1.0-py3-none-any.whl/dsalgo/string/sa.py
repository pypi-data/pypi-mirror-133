import typing

from kagemeka.dsa.misc.compress_array import CompressArray


def sa_is(a: list[int]) -> list[int]:
    mn = min(a)
    a = [x - mn + 1 for x in a]
    a.append(0)
    n = len(a)
    m = max(a) + 1
    is_s = [True] * n
    for i in range(n - 2, -1, -1):
        is_s[i] = is_s[i + 1] if a[i] == a[i + 1] else a[i] < a[i + 1]
    is_lms = [not is_s[i - 1] and is_s[i] for i in range(n)]
    lms = [i for i in range(n) if is_lms[i]]
    bucket = [0] * m
    for x in a:
        bucket[x] += 1

    def induce() -> list[int]:
        sa = [-1] * n
        sa_idx = bucket.copy()
        for i in range(m - 1):
            sa_idx[i + 1] += sa_idx[i]
        for i in lms[::-1]:
            sa_idx[a[i]] -= 1
            sa[sa_idx[a[i]]] = i

        sa_idx = bucket.copy()
        s = 0
        for i in range(m):
            s, sa_idx[i] = s + sa_idx[i], s
        for i in range(n):
            i = sa[i] - 1
            if i < 0 or is_s[i]:
                continue
            sa[sa_idx[a[i]]] = i
            sa_idx[a[i]] += 1

        sa_idx = bucket.copy()
        for i in range(m - 1):
            sa_idx[i + 1] += sa_idx[i]
        for i in range(n - 1, -1, -1):
            i = sa[i] - 1
            if i < 0 or not is_s[i]:
                continue
            sa_idx[a[i]] -= 1
            sa[sa_idx[a[i]]] = i
        return sa

    sa = induce()
    lms_idx = [i for i in sa if is_lms[i]]
    l = len(lms_idx)
    rank = [-1] * n
    rank[-1] = r = 0
    for i in range(l - 1):
        j, k = lms_idx[i], lms_idx[i + 1]
        for d in range(n):
            j_is_lms, k_is_lms = is_lms[j + d], is_lms[k + d]
            if a[j + d] != a[k + d] or j_is_lms ^ k_is_lms:
                r += 1
                break
            if d > 0 and j_is_lms | k_is_lms:
                break
        rank[k] = r
    rank = [i for i in rank if i >= 0]
    if r == l - 1:
        lms_order = [-1] * l
        for i, r in enumerate(rank):
            lms_order[r] = i
    else:
        lms_order = sa_is(rank)
    lms = [lms[i] for i in lms_order]
    return induce()[1:]


def sa_doubling(a: list[int]) -> list[int]:
    n = len(a)
    rank, k = CompressArray()(a), 1
    while True:
        key = [r << 30 for r in rank]
        for i in range(n - k):
            key[i] |= 1 + rank[i + k]
        sa = sorted(range(n), key=lambda x: key[x])
        rank[sa[0]] = 0
        for i in range(n - 1):
            rank[sa[i + 1]] = rank[sa[i]] + (key[sa[i + 1]] > key[sa[i]])
        k <<= 1
        if k >= n:
            break
    return sa


def sa_doubling_countsort(a: list[int]) -> list[int]:
    n = len(a)

    def counting_sort_key(a):
        cnt = [0] * (n + 2)
        for x in a:
            cnt[x + 1] += 1
        for i in range(n):
            cnt[i + 1] += cnt[i]
        key = [0] * n
        for i in range(n):
            key[cnt[a[i]]] = i
            cnt[a[i]] += 1
        return key

    rank, k = CompressArray()(a), 1
    while True:
        second = [0] * n
        for i in range(n - k):
            second[i] = 1 + rank[i + k]
        rank_second = counting_sort_key(second)
        first = [rank[i] for i in rank_second]
        rank_first = counting_sort_key(first)
        sa = [rank_second[i] for i in rank_first]
        key = [first[i] << 30 | second[j] for i, j in zip(rank_first, sa)]
        rank[sa[0]] = 0
        for i in range(n - 1):
            rank[sa[i + 1]] = rank[sa[i]] + (key[i + 1] > key[i])
        k <<= 1
        if k >= n:
            break
    return sa
