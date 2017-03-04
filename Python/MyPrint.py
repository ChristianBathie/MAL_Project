class MyPrint:

    @staticmethod
    def unicode(output):
        try:
            print(output)
        except UnicodeEncodeError:
            for c in output:
                try:
                    print(c, end='')
                except UnicodeEncodeError:
                    print('[unicode]', end='')
            print()