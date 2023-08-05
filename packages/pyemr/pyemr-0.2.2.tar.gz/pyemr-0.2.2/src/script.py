import sys
import pandas as pd
import numpy as np
import databricks.koalas as ks
from pyspark.sql import SparkSession

kdf = ks.DataFrame(
{'a': [1, 2, 3, 4, 5, 6],
 'b': [100, 200, 300, 400, 500, 600],
 'c': ["one", "two", "three", "four", "five", "six"]},
index=[10, 20, 30, 40, 50, 60])

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))