def calculate_gini_impurity(z):
    # ... add your Python code here ...
    n = len(z)
    if n == 0:
        return 0

    yes_count = 0
    no_count = 0

    for label in z:
        if label == 'yes':
            yes_count += 1
        elif label == 'no':
            no_count += 1

    p_yes = yes_count / n
    p_no = no_count / n

    return 1 - (p_yes ** 2 + p_no ** 2)


# Test examples
assert calculate_gini_impurity(['yes', 'no']) == 1/2
assert calculate_gini_impurity(['yes', 'yes', 'no']) == 4/9


def split_dataset(x, y, z, threshold):
    # ... add your Python code here ...
    Lx, Ly, Lz = [], [], []
    Rx, Ry, Rz = [], [], []

    for i in range(len(z)):
        if x[i] <= threshold:
            Lx.append(x[i])
            Ly.append(y[i])
            Lz.append(z[i])
        else:
            Rx.append(x[i])
            Ry.append(y[i])
            Rz.append(z[i])

    return (Lx, Ly, Lz, Rx, Ry, Rz)


# Test example
aa = split_dataset([2, 3], [5, 7], ['yes', 'no'], 2)
assert aa == ([2], [5], ['yes'], [3], [7], ['no'])
assert isinstance(aa, tuple)


def gini_change(parent_z, left_z, right_z):
    gini_parent = calculate_gini_impurity(parent_z)
    gini_left = calculate_gini_impurity(left_z)
    gini_right = calculate_gini_impurity(right_z)
    n_parent = len(parent_z)
    n_left = len(left_z)
    n_right = len(right_z)
    delta_gini = gini_parent - ((n_left / n_parent) * gini_left +
    (n_right / n_parent) * gini_right)
    return(delta_gini)


# Test examples
assert gini_change(['yes', 'no'], ['yes'], ['no']) == 1/2
assert gini_change(['yes', 'yes', 'no'], ['yes', 'yes'], ['no']) == 4/9
assert gini_change(['yes', 'yes', 'no'], ['yes', 'no'], ['yes']) == 1/9


def investigate_best_split():
    # ... add your Python code here ...
    x = [1, 2, 3, 4, 5, 6]
    y = [10, 20, 30, 40, 50, 60]
    z = ['yes', 'yes', 'yes', 'no', 'no', 'no']

    print("Parent gini:", calculate_gini_impurity(z))

    best_threshold = None
    best_delta = 0

    for i in range(len(x)):
        T = x[i]
        Lx, Ly, Lz, Rx, Ry, Rz = split_dataset(x, y, z, T)

        if len(Lz) == 0 or len(Rz) == 0:
            continue

        delta = gini_change(z, Lz, Rz)
        print("threshold =", T, "delta_gini =", delta, "left_z =", Lz, "right_z =", Rz)

        if delta > best_delta:
            best_delta = delta
            best_threshold = T

    print("Best threshold:", best_threshold, "with delta_gini:", best_delta)


def find_best_split(x, y, z):
    best_delta = 0
    best_threshold = None
    for i in range(0, len(z)):
        T = x[i]
        Lx, Ly, Lz, Rx, Ry, Rz = split_dataset(x, y, z, T)
        # ... add your Python code here ...
        if len(Lz) == 0 or len(Rz) == 0:
            continue

        delta = gini_change(z, Lz, Rz)
        if delta > best_delta:
            best_delta = delta
            best_threshold = T

    return(best_threshold)


def build_tree(x, y, z, depth):
    node = {'x':x, 'y':y, 'z':z, 'left':None, 'right':None,
    'threshold':None}
    T = find_best_split(x, y, z)
    if (T != None):
        Lx, Ly, Lz, Rx, Ry, Rz = split_dataset(node['x'], node['y'], node['z'], T)
        if (depth == 1):
            left_child = {'x':Lx, 'y':Ly, 'z':Lz, 'left':None,
            'right':None, 'threshold':None}
            right_child = {'x':Rx, 'y':Ry, 'z':Rz, 'left':None,
            'right':None, 'threshold':None}
        else:
            left_child = build_tree(Ly, Lx, Lz, depth + 1)
            right_child = build_tree(Ry, Rx, Rz, depth + 1)
        node['left'] = left_child
        node['right'] = right_child
        node['threshold'] = T
    return(node)


# Test example
bb = build_tree([148, 85, 183, 89, 137, 116],
[50, 31, 32, 21, 33, 30],
['yes', 'no', 'yes', 'no', 'yes', 'no'], 0)
print(bb)

investigate_best_split()

# Part (c) sample output and conclusion:
# Parent gini: 0.5
# threshold = 1 delta_gini = 0.1 ...
# threshold = 2 delta_gini = 0.25 ...
# threshold = 3 delta_gini = 0.5 ...
# threshold = 4 delta_gini = 0.25 ...
# threshold = 5 delta_gini = 0.1 ...
# Best threshold: 3 with delta_gini: 0.5
#
# Conclusion:
# Threshold 3 gives the largest decrease in impurity (0.5) and perfectly
# separates all 'yes' values from all 'no' values in this dataset.

# Part (e):
# From the printed output tree (for the given test data):
# [x <= 116?]
# ├── Yes  -> class 'no'  (pure leaf)
# └── No   -> class 'yes' (pure leaf)
#
# Suggested improvement:
# Add an early stopping rule so splitting stops when a node is pure
# (all labels same) or when impurity gain is zero.
#
# If x and y are swapped:
# The threshold value changes because a different feature is split first,
# but this tiny dataset is still perfectly separable in one split.
