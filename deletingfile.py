import os

for i in os.listdir("cache"):
    os.remove("cache/"+i)