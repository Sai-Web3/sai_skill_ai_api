import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity


if __name__ == '__main__':
    target = np.random.rand(1, 12000)
    queries =np.random.rand(100, 12000)

    start = time.time()
    cosine_similarity(target, queries)
    print(start - time.time())
