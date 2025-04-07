import re
from datetime import datetime
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

logfile = "luka_kukhaleishvili_1_server.log"

# Sample log format regex
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<http>HTTP/\d\.\d)" \d+ \d+ ".*?" ".*?" (?P<responsetime>\d+)'
)

request_times = defaultdict(int)

with open(logfile, 'r') as f:
    for line in f:
        match = log_pattern.search(line)
        if match:
            time_str = match.group("time").split("+")[0]  # Remove timezone offset
            timestamp = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            minute = timestamp.replace(second=0)
            request_times[minute] += 1

df = pd.DataFrame(list(request_times.items()), columns=["Time", "Request_Count"])
df.sort_values("Time", inplace=True)


threshold = df['Request_Count'].mean() + 3 * df['Request_Count'].std()
ddos_minutes = df[df['Request_Count'] > threshold]

plt.figure(figsize=(12,6))
plt.plot(df["Time"], df["Request_Count"], label="Requests per Minute")
plt.axhline(threshold, color="red", linestyle="--", label="DDoS Threshold")
plt.xlabel("Time")
plt.ylabel("Requests")
plt.title("DDoS Detection Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("ddos_detection_graph.png")
plt.show()

# Output possible DDoS times
print("Possible DDoS Attack Times:")
print(ddos_minutes)
