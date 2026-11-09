
import unittest

from afrilabel_qa import validate_coco


class ValidatorTests(unittest.TestCase):
    def test_detects_known_sample_issues(self):
        data = {
            "images": [{"id": 1, "file_name": "demo.jpg", "width": 100, "height": 100}],
            "categories": [{"id": 1, "name": "person"}],
            "annotations": [
                {"id": 1, "image_id": 1, "category_id": 1, "bbox": [10, 10, 20, 20]},
                {"id": 2, "image_id": 1, "category_id": 1, "bbox": [90, 90, 20, 20]},
                {"id": 3, "image_id": 1, "category_id": 1, "bbox": [10, 10, 0, 20]},
            ],
        }
        report = validate_coco(data)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("BOX_OUT_OF_BOUNDS", codes)
        self.assertIn("NON_POSITIVE_SIZE", codes)
        self.assertEqual(report["status"], "FAIL")

    def test_clean_dataset_passes(self):
        data = {
            "images": [{"id": 1, "file_name": "demo.jpg", "width": 100, "height": 100}],
            "categories": [{"id": 1, "name": "person"}],
            "annotations": [
                {"id": 1, "image_id": 1, "category_id": 1, "bbox": [10, 10, 20, 20]}
            ],
        }
        report = validate_coco(data)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["error_count"], 0)
        self.assertEqual(report["warning_count"], 0)


if __name__ == "__main__":
    unittest.main()
