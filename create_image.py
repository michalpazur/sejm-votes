import json, math
from PIL import Image, ImageDraw
from matplotlib.pylab import get_cmap

def average(arr):
    return sum(arr)/len(arr)

with open('vote_results_2.json', 'r') as f:
    results = json.load(f)

avgs = {}
std_vars = {}
corrs = {}
length = len(results['PiS'])

for key in results:
    avgs[key] = average(results[key])

for key in results:
    std_var = 0
    for i in range(len(results[key])):
        value = (results[key][i] - avgs[key]) ** 2
        std_var += (results[key][i] - avgs[key]) ** 2
    std_vars[key] = math.sqrt(std_var)

print(std_vars)

x = 0
for key_x in results:
    y = 0
    for key_y in results:
        cov = 0
        for i in range(length):
            value = (results[key_x][i] - avgs[key_x]) * (results[key_y][i] - avgs[key_y])
            cov += value
        corr = cov / (std_vars[key_x] * std_vars[key_y])
        print(key_x, key_y, corr)
        arr = corrs.setdefault(key_x, [])
        arr.append(corr)
        corrs[key_x] = arr
    x += 1

print(corrs)
sorted_results_keys = sorted(list(corrs.keys()), key=lambda key: average(corrs[key]))
print(sorted_results_keys)
sorted_results = {}
for key in sorted_results_keys:
    sorted_results[key] = results[key]

img = Image.new('RGBA', (3000, 3000))
x = 0
for key_x in sorted_results:
    y = 0
    for key_y in sorted_results:
        cov = 0
        for i in range(length):
            value = (results[key_x][i] - avgs[key_x]) * (results[key_y][i] - avgs[key_y])
            cov += value
        corr = cov / (std_vars[key_x] * std_vars[key_y])
        print(key_x, key_y, corr)
        d = ImageDraw.Draw(img)
        fill_color = tuple(int(x * 255) for x in get_cmap('RdYlGn')((corr + 1) / 2))
        d.rectangle([(x * 500, y * 500), ((x + 1) * 500, (y+ 1) * 500)], fill=fill_color)
        y += 1
    x += 1
img.save('chart.png')
