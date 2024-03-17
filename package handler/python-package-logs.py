sc_logs = open("packages received.log").read().split("\n")
py_logs = open("python logs.log").read().replace("sent package: ","").split("\n")

off = 0
for line,_ in enumerate(py_logs):
    if not (py_logs[line] == sc_logs[line - off]):
        print(line)
        off += 1
