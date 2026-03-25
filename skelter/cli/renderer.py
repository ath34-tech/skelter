def render_tree(folders, files):
    tree = {}

    for folder in folders:
        parts = folder.split("/")
        cur = tree
        for p in parts:
            cur = cur.setdefault(p, {})

    def _print(d, indent=0):
        for k, v in d.items():
            print("  " * indent + f"{k}/")
            _print(v, indent + 1)

    _print(tree)

    for f in files:
        print(f)