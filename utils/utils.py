import subprocess
import timeit

def executor(module):
    if module:
        start_time = timeit.default_timer()
        cwd = os.getcwd()
        cmd = "python "
        os.chdir(module.split('\\')[0])
        cmd += module.split('\\')[1]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.decode().split("\n")
        for line in result:
            if not line.startswith('#'):
                print(line)
        print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))
        os.chdir(cwd)
