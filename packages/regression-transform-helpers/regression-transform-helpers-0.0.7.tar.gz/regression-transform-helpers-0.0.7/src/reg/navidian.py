from sklearn.preprocessing import OneHotEncoder

from scipy.sparse import csr_matrix

class NavidianEncoder(OneHotEncoder):
    def transform(self, X):
        transformed = super().transform(X)
        
        feats = self.get_feature_names_out().tolist()

        if 'badge_model_None' in feats:
            idx_bm_none = feats.index('badge_model_None')
            transformed = transformed[:, :idx_bm_none]

        if 'series_model_None' in feats:
            idx_sm_none = feats.index('series_model_None')
            transformed = transformed[:, :idx_sm_none]

        if 'badge_None' in feats:
            idx_b_none = feats.index('badge_None')
            transformed = transformed[:, :idx_b_none]
        if 'series_None' in feats:
            idx_s_none = feats.index('series_None')
            transformed = transformed[:, :idx_s_none]

        transformed = csr_matrix(transformed)

        return transformed
