filepath = open('groundtruth.txt')# open('sockpuppet.txt')
ori = filepath.readlines()
filepath.close()

dup = '1001000002'

wf = open('0new_sockpuppet.txt', 'w')
uf=open('new_user.txt', 'w')
new = []
i = 0
for items in ori:
    tmps = items.strip().split()
    i += 1
    for elem in tmps:
        if not new.__contains__(elem):
            new.append(elem)
            uf.write(elem+'\n')
    if not tmps.__contains__(dup):
        wf.write(' '.join(tmps) + '\n')
    else:
        if len(tmps) > 2:
            tmps.remove(dup)
            wf.write(' '.join(tmps) + '\n')
wf.close()
uf.close()
print('user length:', len(new))
print('sockpuppet length:', i)


