class Loader:
    CLASSES_FILE = "data/parameters/classes.names"

    __sponges_classes = {}

    @staticmethod
    def SpongesClasses() -> dict[int, str]:
        if len(Loader.__sponges_classes) == 0:

            with open(Loader.CLASSES_FILE, 'rt') as f:
                for i, name in enumerate(f.readlines()):
                    name = name.rstrip("\n")
                    Loader.__sponges_classes[i] = name

        return Loader.__sponges_classes
