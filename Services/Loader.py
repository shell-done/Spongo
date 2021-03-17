class Loader:
    CLASSES_FILE_PATH = "data/parameters/classes.names"
    STYLE_FILE_PATH = "data/assets/style.qss"

    _sponges_classes = {}

    @staticmethod
    def SpongesClasses() -> dict[int, str]:
        if len(Loader._sponges_classes) == 0:

            with open(Loader.CLASSES_FILE_PATH, 'rt') as f:
                for i, name in enumerate(f.readlines()):
                    name = name.rstrip("\n")
                    Loader._sponges_classes[i] = name

        return Loader._sponges_classes


    @staticmethod
    def PreprocessedQSS() -> str:
        with open(Loader.STYLE_FILE_PATH, "r") as qss_file:
            lines = [l.rstrip("\n") for l in qss_file.readlines()]

        qss_vars = {}
        qss_body = ""

        for i, l in enumerate(lines):
            l = l.strip()
            if len(l) == 0:
                continue

            if l[0] == "@":
                if not l.endswith(";"):
                    print("[WARNING] QSSPreprocessor : Parsing error at line %d for '%s' (missing semicolon)" % (i, l))

                l = l.rstrip(";")
                s = l.split(":")
                if len(s) < 2:
                    print("[WARNING] QSSPreprocessor : Parsing error at line %d for '%s' (missing colon)" % (i, l))
                    continue

                qss_vars[s[0].strip()] = s[1].strip()
            else:
                qss_body += l

        qss_vars_names = list(qss_vars.keys())
        qss_vars_names.sort()
        qss_vars_names.reverse()
        for k in qss_vars_names:
            qss_body = qss_body.replace(k, qss_vars[k])
        
        return qss_body
