class AppInfo:
    @staticmethod
    def isDevMode():
        return False

    @staticmethod
    def version():
        dev_suffix = "(dev version)" if AppInfo.isDevMode() else ""

        return "Beta 0.9 %s" % dev_suffix
