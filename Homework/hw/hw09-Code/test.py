def makeChange(total, biggest):
    ans = []

    def make_change(total, biggest, L):
        if total == 0:
            ans.append(L[:])
            return
        if biggest == 0:
            return
        if biggest <= total:  # use it
            L.append(biggest)
            make_change(total - biggest, biggest, L)
            L.pop()
        make_change(total, biggest - 1, L)

    make_change(total, biggest, [])
    return ans


a = int(input())
b = int(input())
print(makeChange(a, b))
