my_arr = ["hi", "hello", "bye"]

all_labels = [f"element is: {itm}" for itm in my_arr]

with open("output.tsv", "w", encoding="utf-8") as f:
    f.write("\t".join(map(str, all_labels)) + "\n")

print(my_arr)
print(all_labels)