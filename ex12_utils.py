from copy import deepcopy
board = [['a', 'y', 'ar', 'x'], ['a', 's', 'd', 'g'], ['a', 'r', 'l', 'k'], ['k', 'l', 'asd', 'd']]
#path = [(0,0),(0,1),(0,2)]
words = ['arx','asd','nii']

# words = ["anoxg","krjxa"]
# words = ["ado","xgd","a","aya","dark"]

""":return a list of the coord neighboors"""
def neighbors_list(coord, board):
    y = coord[0]
    x = coord[1]
    lst = []
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if (i, j) != coord:
                lst.append((i, j))
    legal_lst = []
    for location in lst:
        if location[0] >= 0 and location[1] >= 0 and location[0] < len(board) and location[1] < len(board[0]):
            legal_lst.append(location)
    return legal_lst

"""bilds a word from bord with a given path
   :return a word string
"""
def build_word(board, path):
    word = ""
    for p in path:
        word = word + board[p[0]][p[1]]
    return word


# print(build_word(board,path))

"""checks if the path is valid according to rules
    :return a bool of the answer"""
def is_valid_path(board, path, words):
    path_set = set(path)
    for p in path:
        if p[0]<0 or p[0]>=len(board) or p[1]<0 or p[1]>=len(board[0]):
            return None
    for p in range(len(path) - 1):
        legal_neighbors = neighbors_list(path[p], board)
        if path[p + 1] not in legal_neighbors:
            return None
    word = build_word(board, path)
    if word in words and len(path_set) == len(path):
        return word
    return None

"""checks if a word is in a list of words"""
def check_word(str, words):
    count = 0
    for word in words:
        count = 0
        if len(str) <= len(word):
            for i in range(len(str)):
                if str[i] == word[i]:
                    count += 1
                if count == len(str):
                    return True
    return False


"""finds the neighbors that are not used is path"""
def find_correct_neighbors(path, neighbors):
    good_neighbers = []
    for neighbor in neighbors:
        if neighbor not in path:
            good_neighbers.append(neighbor)
    return good_neighbers


"""find all paths in bord that their path length is n and starting from a given coordinate
    :return True if i did and False if not"""
def find_length_n_paths_helper(n, board, words, path, paths, coord):
    flag = False
    cur_coord = coord
    if n == len(path):
        word = build_word(board, path)
        if word in words:
            lis =deepcopy(path)
            paths.append(lis)
            return True
        return False
    if len(path) != 0:
        cur_coord = path[-1]
    neighbors = neighbors_list(cur_coord, board)
    good_neighbors = find_correct_neighbors(path, neighbors)
    for neighbor in good_neighbors:
        if not check_word(build_word(board, path), words):
            continue
        path.append(neighbor)
        flag = find_length_n_paths_helper(n, board, words, path, paths, neighbor)
        path.pop()
    if flag:
        return True
    return False

"""find all paths in bord that their path is n long
    :return a list of lists that contain paths"""
def find_length_n_paths(n, board, words):
    paths = []
    path = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            p = (i, j)
            path.append(p)
            find_length_n_paths_helper(n, board, words, path, paths, (i, j))
            path = []
    return paths

"""find all paths in bord that their word length is n and starting from a given coordinate
    :return True if i did and False if not"""
def find_length_n_words_helper(n, board, words, path, paths, coord):
    flag = False
    cur_coord = coord
    word = build_word(board, path)
    if n == len(word):
        if word in words:
            lis = deepcopy(path)
            paths.append(lis)
            return True
        return False
    if len(path) != 0:
        cur_coord = path[-1]
    neighbors = neighbors_list(cur_coord, board)
    good_neighbors = find_correct_neighbors(path, neighbors)
    for neighbor in good_neighbors:
        if not check_word(build_word(board, path), words):
            continue
        path.append(neighbor)
        flag = find_length_n_words_helper(n, board, words, path, paths, neighbor)
        path.pop()
    if flag:
        return True
    return False

"""find all paths in bord that their word is n long
    :return a list of lists that contain paths"""
def find_length_n_words(n, board, words):
    paths = []
    path = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            p = (i, j)
            path.append(p)
            find_length_n_words_helper(n, board, words, path, paths, (i, j))
            path = []
    return paths

""":return the paths that gives the max score to given wwords"""
def max_score_paths(board, words):
    words_paths_dict = {}
    ls = []
    word = ""
    for i in range(16):
        ls = find_length_n_paths(i , board, words)
        for path in ls:
            word = build_word(board,path)
            words_paths_dict[word] = path
    vals = words_paths_dict.values()
    return list(vals)
