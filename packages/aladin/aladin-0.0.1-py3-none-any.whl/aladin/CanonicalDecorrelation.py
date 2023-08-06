import numpy as np
from numpy.testing import assert_array_almost_equal
from scipy.stats import pearsonr
from sklearn.cross_decomposition import PLSCanonical

class CanonicalDecorrelation(PLSCanonical):
    """
    """
    def __init__(
        self, 
        X=[], 
        Y=[],
        n_deflations=None,
        test_dec=10,
        _n_components=1,
        *,
        scale=False,
        algorithm="svd"
        ):
        
        self.X = self._center_scale(X, scale=scale)
        self.Y = self._center_scale(Y, scale=scale)
        self.n_deflations = n_deflations
        self.test_dec = test_dec
        
        # Set number of deflation steps
        if self.n_deflations is None:
            self.n_deflations = min(self.X.shape[1], self.Y.shape[1])
        assert self.n_deflations <= min(self.X.shape[1], self.Y.shape[1]),\
            'Cannot deflate more than data dimensions'
        
        # Init dicts to store deflated matrices
        self.Xd = {}
        self.Yd = {}
        # Init with original matrices
        self.Xd[0] = self.X
        self.Yd[0] = self.Y

        # Init dict to store weights and loadings for testing
        self.test = {}
        self.test['x_loadings'] = np.zeros((
            self.X.shape[1], self.n_deflations))
        self.test['x_weights'] = np.zeros((
            self.X.shape[1], self.n_deflations))
        self.test['y_loadings'] = np.zeros((
            self.Y.shape[1], self.n_deflations))
        self.test['y_weights'] = np.zeros((
            self.Y.shape[1], self.n_deflations))

        super().__init__(
            n_components=_n_components,
            scale=scale,
            algorithm=algorithm,
        )

    def _center_scale(self, M, scale=True):
        """Center M and scale if the scale parameter==True
        Returns
        -------
            M
        """
        # center
        m_mean = M.mean(axis=0)
        M -= m_mean
        # scale
        if scale:
            m_std = M.std(axis=0, ddof=1)
            m_std[m_std == 0.0] = 1.0
            M /= m_std
        return M
    
    def deflate(self):
        """
        """
        assert self.n_components == 1,\
            'Deflation must happen one step at a time'
        # Init dicts to store scores for covariance analysis
        self.x_scores = {}
        self.y_scores = {}
        # Deflate
        for k in range(self.n_deflations):
            self.fit(self.Xd[k], self.Yd[k])
            self.x_scores[k] = np.dot(self.Xd[k], self.x_weights_)
            self.y_scores[k] = np.dot(self.Yd[k], self.y_weights_)
            self.Xd[k+1] = self.Xd[k] - np.outer(
                self.x_scores[k], 
                self.x_loadings_)
            self.Yd[k+1] = self.Yd[k] - np.outer(
                self.y_scores[k], 
                self.y_loadings_)
            # Save params for testing
            self.test['x_loadings'][:, k] = self.x_loadings_.flatten()
            self.test['x_weights'][:, k] = self.x_weights_.flatten()
            self.test['y_loadings'][:, k] = self.y_loadings_.flatten()
            self.test['y_weights'][:, k] = self.y_weights_.flatten()

    def corrcoef(self):
        """
        """
        assert hasattr(self, 'x_scores'), 'Run deflate() first'
        self.pearson_rp = np.zeros((len(self.x_scores), 2))
        for i, (x_key, y_key) in enumerate(zip(self.x_scores, self.y_scores)):
            self.pearson_rp[i, :] = np.asarray(pearsonr(
                self.x_scores[x_key].flatten(), 
                self.y_scores[y_key].flatten()))
    
    def test_deflation(self):
        self.test_sanity_check_weights()
        self.test_sanity_check_ranks()

    def test_sanity_check_weights(self):
        """
        """
        # Do full PLSC
        plsca = PLSCanonical(
            n_components=self.n_deflations, 
            algorithm=self.algorithm, 
            scale=self.scale)
        plsca.fit(self.X, self.Y)
        # Check params against auto pipeline
        assert_array_almost_equal(plsca.x_weights_, self.test['x_weights'],\
                decimal=self.test_dec, err_msg='Discrepancy in x_weights')
        assert_array_almost_equal(plsca.x_loadings_, self.test['x_loadings'],\
                decimal=self.test_dec, err_msg='Discrepancy in x_loadings')
        assert_array_almost_equal(plsca.y_weights_, self.test['y_weights'],\
                decimal=self.test_dec, err_msg='Discrepancy in y_weights')
        assert_array_almost_equal(plsca.y_loadings_, self.test['y_loadings'],\
                decimal=self.test_dec, err_msg='Discrepancy in y_loadings')
    
    def test_sanity_check_ranks(self):
        """
        """
        ranks = []
        for x_key, y_key in zip(self.Xd, self.Yd):
            cov_matrix = np.dot(self.Xd[x_key].T, self.Yd[y_key])
            if cov_matrix.max() < np.finfo(cov_matrix.dtype).eps:
                break
            ranks.append(np.linalg.matrix_rank(cov_matrix))
        assert np.all(np.diff(ranks) == np.ones(len(ranks) - 1) * -1),\
            'Ranks of cross-correlation matrices are not \
                monotonically decreasing'