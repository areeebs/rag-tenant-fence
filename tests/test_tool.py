import unittest

from tool import audit


class FenceTests(unittest.TestCase):
    def test_cross_tenant_retrieval_fails(self):
        report = audit({
            "documents": [{"id": "d1", "tenant_id": "A", "source": "kb/a"}],
            "queries": [{"id": "q1", "tenant_id": "B", "retrieved_ids": ["d1"]}],
        })
        self.assertFalse(report["pass"])
        self.assertEqual("cross_tenant_result", report["findings"][0]["code"])

    def test_missing_document_fails_closed(self):
        report = audit({"documents": [], "queries": [{"tenant_id": "A", "retrieved_ids": ["missing"]}]})
        self.assertFalse(report["pass"])
        self.assertEqual("unknown_document", report["findings"][0]["code"])

    def test_same_tenant_with_source_passes(self):
        report = audit({
            "documents": [{"id": "d1", "tenant_id": "A", "source": "kb/a"}],
            "queries": [{"tenant_id": "A", "retrieved_ids": ["d1"]}],
        })
        self.assertTrue(report["pass"])


if __name__ == "__main__":
    unittest.main()
