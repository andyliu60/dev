def triangles(max):
    n = 1
    L1 = [1]
    yield L1
    L2 = [1, 1]
    while n < max:
        yield L2
        L3 = []
        i = 0
        while i < len(L2)-1:
            a = L2[i] + L2[i+1]
            L3.append(a)
            i += 1
        L3.insert(0,1)
        L3.append(1)
        L2 = L3
        n+=1
