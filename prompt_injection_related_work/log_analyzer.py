log_paths = [
    'logs\\2026-03-23_21-02-05\\2026-03-23_21-18-43_manual_flush.txt',
    'logs\\2026-03-24_09-22-46\\2026-03-24_09-42-24_manual_flush.txt'
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


attempt_key = 'posting'
successed_key = 'additional'

redundancy_attempt = 0 # of lines that contain keys but each of them has no experimental value.
redundancy_successed = 0

lines_per_access = 3

attempt = (logs.count(attempt_key) - redundancy_attempt) / lines_per_access
successed = (logs.count(successed_key) - redundancy_successed) / lines_per_access

print(f'total attempt: {attempt}')
print(f'total successed: {successed}')
print(f'ASR: {successed / attempt}')