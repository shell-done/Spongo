class AppInfo:
    @staticmethod
    def isDevMode():
        return False

    @staticmethod
    def version():
        dev_suffix = "(dev)" if AppInfo.isDevMode() else ""

        return "Version R-1.0 %s" % dev_suffix
