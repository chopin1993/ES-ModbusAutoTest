from fnmatch import fnmatch

if __name__ == '__main__':
    data = b'\xd7e\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01'
    print(data)
    datalist = list(data)
    print(datalist)

    log = "9F190021000091021800007E22E0050059899201AA050712C0010083D2A82022"
    print(fnmatch(log, "*7E*050712C00100*"))

    log = r'{"cmd":"write","deviceKey":"0000NSU7","function":{"channel_collection":[{"channel":1,"switch":false},{"channel":2,"switch":false},{"channel":3,"switch":false},{"channel":4,"switch":false}]},"sno":"6-16-15-1"}'
    print(fnmatch(log, r'*"function":{"channel_collection":[{"channel":1,"switch":false}*'))
