import time
import signal

def timeout(s):
    def _timeout(f):
        def handler(signum, frame):
            print("DEBUG: TIMEOUT ERROR")
            raise TimeoutError()
        def wrapper(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(s)
            try:
                res = f(*args)
            except TimeoutError:
                res = None
                timeout_error = True
            else:
                timeout_error = False
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, signal.SIG_DFL)
            return timeout_error, res
        return wrapper
    return _timeout

@timeout(1)
def f_ok():
    for _ in range(10000000):
        pass

@timeout(1)
def f_err():
    for _ in range(1000000000):
        pass

@timeout(2)
def f_err2():
    for _ in range(1000000000):
        pass

# Check all fine
timeout_error, res = f_ok()
assert not timeout_error, "Timeout in f_ok. Bad assertion error"
# Check last alarm is turned off
time.sleep(2)
timeout_error, res = f_ok()
assert not timeout_error, "Timeout in f_ok. Bad assertion error"
# 
timeout_error, res = f_err()
assert timeout_error, "No timeout in f_err. Bad assertion error"
timeout_error, res = f_err2()
assert timeout_error, "No timeout in f_err2. Bad assertion error"
timeout_error, res = f_err()
assert timeout_error, "No Timeout in f_err. Bad assertion error"
print("All OK!")
