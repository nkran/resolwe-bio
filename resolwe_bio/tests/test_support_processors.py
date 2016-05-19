# pylint: disable=missing-docstring
from .utils import skipDockerFailure, BioProcessTestCase


class CompatibilityProcessorTestCase(BioProcessTestCase):

    def test_reference_compatibility(self):
        mapping = self.prepare_bam()
        genome = self.prepare_genome('sp_test.fasta')
        annotation = self.prepare_annotation()

        inputs = {'reference': genome.pk, 'bam': mapping.pk, 'annot': annotation.pk}
        compatibility_test = self.run_processor('reference_compatibility', inputs)
        self.assertFiles(compatibility_test, 'report_file', 'sp_test_compatibility_report.txt')

    @skipDockerFailure("Errors with: int() argument must be a string or a "
        "number, not 'dict' at self.assertJSON(features, "
        "features.output['feature_location'], '', 'feature_locations.json.gz')")
    def test_feature_location(self):
        inputs = {'src': 'mm10_small.gtf.gz'}
        annotation = self.run_processor('upload-gtf', inputs)

        inputs = {'annotation': annotation.pk,
                  'feature_type': 'exon',
                  'id_type': 'transcript_id',
                  'summarize_exons': True}
        features = self.run_processor('feature_location', inputs)
        self.assertJSON(features, features.output['feature_location'], '', 'feature_locations.json.gz')
