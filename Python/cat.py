import sys

def cat_path():
    dic = {}

    cat = int(sys.stdin.readline())
    cat_path = []

    for line in sys.stdin:
        parent = line.split(" ")[0]
        if parent == -1:
            break
        else:
            children = line.split(" ")[1:]

            for element in children:
                dic[int(element)] = int(parent)

    while True:
        cat_path.append(cat)
        try:
            cat = dic[cat]
        except:
            break

    print(*cat_path)

if __name__ == "__main__":
    cat_path()
