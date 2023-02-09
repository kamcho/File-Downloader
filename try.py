import os
from urllib.parse import urlparse

url = "https://img.freepik.com/premium-vector/semi-truck-vector_74218-570.jpg?w=2000"
a = urlparse(url)
print(a.path)                    # Output: /kyle/09-09-201315-47-571378756077.jpg
print(os.path.basename(a.path))
url="https://img.freepik.com/premium-vector/semi-truck-vector_74218-570.jpg?w=2000"
