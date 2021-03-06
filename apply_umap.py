import umap
import time
import pickle

from sklearn.neighbors import KDTree

def run(**kwargs):
  t0 = time.time()
  path = 'data/'
  preprocess_df = pickle.load(open(path + 'preprocess_df.pkl', 'rb'))

  umap_mapper = umap.UMAP(
    n_components=kwargs['components'],
    n_neighbors=kwargs['n_neighbors'],
    min_dist=kwargs['min_dist'],
    metric=kwargs['metric'], # ideally hellinger, but takes ages
    densmap=kwargs['densmap'],
    verbose=True
    )
  mapper = umap_mapper.fit(preprocess_df)
  print('UMAP run in', f'{round(time.time() - t0, 2)}s')
  len(mapper.embedding_)

  t0 = time.time()
  nn = KDTree(mapper.embedding_)
  knn_indices = list(map(lambda x: x.tolist(), nn.query_radius(mapper.embedding_, r=kwargs['threshold'])))
  knn_indices = list(map(lambda elem: [x for x in elem[1] if x != elem[0]], enumerate(knn_indices)))
  
  print('Nearest Neighbors run in', f'{round(time.time() - t0, 2)}s')

  pickle.dump(mapper, open(path + 'umap.pkl', 'wb'))
  pickle.dump(mapper.embedding_, open(path + 'embeddings.pkl', 'wb'))
  pickle.dump(knn_indices, open(path + 'knn_indices.pkl', 'wb'))

if __name__ == '__main__':
  import json
  kwargs = json.load(open('args.json', 'rb'))['apply_umap']
  run(**kwargs)