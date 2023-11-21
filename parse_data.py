import re
import pathlib
import json


file = pathlib.Path(__file__).parent / "data_k.html"
with file.open() as fp:
    file_to_read = fp.read()

print(len(file_to_read))

r1 = r"<script>(DisconSchedule.streets = [\s\S]*)</script>"
options = re.findall(r1, file_to_read)  # returns ['Hello, world!']
print(len(options), "options")

result = options[0].split("\n")

result_result = result[1].split(" = ")
json_result = json.loads(result_result[1])
with open("resulting_list.json", "w", encoding="utf8") as fp:
    json.dump(json_result, fp, indent=4, ensure_ascii=False)
#print(options[0][2000:])