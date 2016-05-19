# pylint: disable=missing-docstring
from .utils import skipDockerFailure, BioProcessTestCase


class PcaProcessorTestCase(BioProcessTestCase):

    @skipDockerFailure("Errors with: ERROR: basic:json value in exp_json not "
        "ObjectId but {u'genes': {u'DPU_G0067108': 0.0, ...}} at "
        "pca = self.run_processor('pca', inputs)")
    def test_pca(self):
        expression_1 = self.prepare_expression(f_rc='exp_1_rc.tab.gz', f_exp='exp_1_tpm.tab.gz', f_type="TPM")
        expression_2 = self.prepare_expression(f_rc='exp_2_rc.tab.gz', f_exp='exp_2_tpm.tab.gz', f_type="TPM")

        inputs = {'exps': [expression_1.pk, expression_2.pk]}
        pca = self.run_processor('pca', inputs)
        self.assertJSON(pca, pca.output['pca'], 'flot.data', 'pca_plot.json.gz')
        self.assertJSON(pca, pca.output['pca'], 'explained_variance_ratios', 'pca_ratios.json.gz')
        self.assertJSON(pca, pca.output['pca'], 'components', 'pca_components.json.gz')

        inputs = {
            'exps': [expression_1.pk, expression_2.pk],
            'genes': ['DPU_G0067096', 'DPU_G0067102', 'DPU_G0067098']
        }

        pca = self.run_processor('pca', inputs)
        self.assertJSON(pca, pca.output['pca'], 'flot.data', 'pca_plot_w_genes.json.gz')

        inputs = {
            'exps': [expression_1.pk, expression_2.pk],
            'genes': ['DPU_G0067098', 'DPU_G0067100', 'DPU_G0067104']  # all zero
        }
        pca = self.run_processor('pca', inputs)

        self.assertJSON(pca, pca.output['pca'], 'flot.data', 'pca_filtered_zeros.json.gz')
        self.assertTrue(pca.output['proc']['warning'])
