import gzip
import shutil

# Compress the file
with open('similarity.pkl', 'rb') as f_in:
    with gzip.open('similarity.pkl.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("File compressed successfully: similarity.pkl.gz")
