import pickle
with open('url.pkl', 'rb') as f:
    mynewlist = pickle.load(f)

print(len(mynewlist))