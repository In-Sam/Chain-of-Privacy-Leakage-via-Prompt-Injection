log_paths = [
    'logs\\2026-03-23_15-22-30\\2026-03-23_15-50-58_analysable.txt',
    'logs\\2026-03-23_17-08-01\\2026-03-23_17-44-06_manual_flush.txt'
]

logs = ''

def append_log(path):
    ln = 0
    f = open(path, 'r')
    text = ''
    while True:
        ln += 1
        line = f.readline()
        if not line:
            print(f'ln: {ln}')
            break
        text += line
    return text

for path in log_paths:
    logs += append_log(path)


attempt_key = 'note'
successed_key = 'additional'

redundancy_attempt = 1 # of lines that contain keys but each of them has no experimental value.
redundancy_successed = 6

lines_per_access = 3

attempt = (logs.count(attempt_key) - redundancy_attempt) / lines_per_access
successed = (logs.count(successed_key) - redundancy_successed) / lines_per_access

print(f'total attempt: {attempt}')
print(f'total successed: {successed}')
print(f'ASR: {successed / attempt}')