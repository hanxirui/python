#/usr/local/env python3

def shell_sort(lists):
	count = len(lists)
	step = 2
	group = count/step
	while group > 0:
		for i in range(0,group):
			j = i + group
			while j < count:
				k = j - group
				key = lists[j]
				while k >= 0:
					if lists[k] > key:
						lists[k + group] = list[k]
						lists[k] = key
					k -= group
				j += group
		group /= step
	return list


if __name__ == "__main__":
    array = [17, 9, 13, 8, 7, -5, 6, 11, 3, 4, 1, 2]
    shell_sort(array)
    print(array)