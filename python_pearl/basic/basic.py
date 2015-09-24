#/usr/local/bin python3
#-*- coding:utf-8 -*-

'''一些python基础知识'''

# 操作技巧
adict = {'Michael': 95, 'Bob': 75, 'Tracy': 85}

alist = [
        '%s--- %s' % (key, value) for key, value in sorted(adict.items())
    ]
print(alist)

# 上面这种方法叫做列表推导法
# 这是另外的例子
print([number * number for number in range(5) ])
# 一个更为复杂和实用的例子
# print([line.split(":")[0] for line in open('/etc/passwd')])

print([ {'name':line.split(":")[0], 'id':line.split(":")[2]}
for line in open('/etc/passwd')
if not line.startswith("#")])

# 遍历目录
import os
fileList = []
rootdir = '..'
for root, subFolders, files in os.walk(rootdir):
	print(subFolders)
	print(files)
    # if '.svn' in subFolders: subFolders.remove('.svn')  # 排除特定目录
print(files)
for file in files:
    file_dir_path = os.path.join(root,file)
    fileList.append(file_dir_path)  
 
print(fileList)




