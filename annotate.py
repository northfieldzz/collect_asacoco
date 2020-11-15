import csv
import cv2

with open('collect.csv') as f, open('annotated_collect.csv', 'w', newline='') as wf:
    reader = csv.DictReader(f)
    writer = csv.writer(wf)
    headers = ['thumbnail', 'title', 'published_date', 'actual']
    writer.writerow(headers)
    for content in reader:
        img = cv2.imread(content['thumbnail'])
        cv2.imshow(content['title'], img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        actual = input()
        writer.writerow([
            content['thumbnail'],
            content['title'],
            content['published_date'],
            actual
        ])
