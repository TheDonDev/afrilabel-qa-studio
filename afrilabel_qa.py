
#!/usr/bin/env python3
"""Validate COCO-style object-detection annotations and produce QA reports."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


def validate_coco(data: dict[str, Any]) -> dict[str, Any]:
    """Return a structured quality report for a COCO-style annotation document."""
    issues: list[dict[str, Any]] = []
    images = {item.get("id"): item for item in data.get("images", [])}
    categories = {item.get("id"): item for item in data.get("categories", [])}
    annotations = data.get("annotations", [])
    seen: set[tuple[Any, ...]] = set()
    class_counts: Counter[str] = Counter()

    def add(severity: str, code: str, annotation_id: Any, message: str) -> None:
        issues.append({
            "severity": severity,
            "code": code,
            "annotation_id": annotation_id,
            "message": message,
        })

    if not images:
        add("ERROR", "NO_IMAGES", "", "The dataset contains no image records.")
    if not categories:
        add("ERROR", "NO_CATEGORIES", "", "The dataset contains no category records.")

    for ann in annotations:
        ann_id = ann.get("id", "")
        image_id = ann.get("image_id")
        category_id = ann.get("category_id")
        bbox = ann.get("bbox")

        if image_id not in images:
            add("ERROR", "UNKNOWN_IMAGE", ann_id,
                f"Annotation references image_id {image_id}, which is not in images.")
        if category_id not in categories:
            add("ERROR", "UNKNOWN_CATEGORY", ann_id,
                f"Annotation references category_id {category_id}, which is not in categories.")
        else:
            class_counts[categories[category_id].get("name", str(category_id))] += 1

        if not isinstance(bbox, list) or len(bbox) != 4:
            add("ERROR", "INVALID_BBOX_FORMAT", ann_id,
                "Bounding box must be [x, y, width, height].")
            continue

        try:
            x, y, width, height = [float(value) for value in bbox]
        except (TypeError, ValueError):
            add("ERROR", "NON_NUMERIC_BBOX", ann_id,
                "Bounding-box coordinates must all be numeric.")
            continue

        if width <= 0 or height <= 0:
            add("ERROR", "NON_POSITIVE_SIZE", ann_id,
                "Bounding-box width and height must both be greater than zero.")
            continue

        image = images.get(image_id)
        if image:
            image_width = image.get("width")
            image_height = image.get("height")
            if isinstance(image_width, (int, float)) and isinstance(image_height, (int, float)):
                if x < 0 or y < 0 or x + width > image_width or y + height > image_height:
                    add("WARNING", "BOX_OUT_OF_BOUNDS", ann_id,
                        f"Bounding box extends outside image dimensions "
                        f"({image_width}x{image_height}).")

        signature = (image_id, category_id, tuple(round(v, 4) for v in (x, y, width, height)))
        if signature in seen:
            add("WARNING", "POSSIBLE_DUPLICATE", ann_id,
                "An identical box with the same image and category appears more than once.")
        seen.add(signature)

    errors = sum(issue["severity"] == "ERROR" for issue in issues)
    warnings = sum(issue["severity"] == "WARNING" for issue in issues)
    return {
        "project": "AfriLabel QA Studio",
        "images_checked": len(images),
        "annotations_checked": len(annotations),
        "categories": len(categories),
        "class_distribution": dict(sorted(class_counts.items())),
        "error_count": errors,
        "warning_count": warnings,
        "status": "PASS" if errors == 0 and warnings == 0 else ("REVIEW" if errors == 0 else "FAIL"),
        "issues": issues,
    }


def write_reports(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "qa_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    with (output_dir / "qa_issues.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["severity", "code", "annotation_id", "message"]
        )
        writer.writeheader()
        writer.writerows(report["issues"])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a COCO-style object-detection annotation JSON file."
    )
    parser.add_argument("annotation_file", type=Path, help="Path to COCO JSON file")
    parser.add_argument("--output", type=Path, default=Path("reports"),
                        help="Directory for JSON and CSV reports (default: reports)")
    args = parser.parse_args()

    try:
        data = json.loads(args.annotation_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Could not read valid JSON: {exc}")

    report = validate_coco(data)
    write_reports(report, args.output)

    print(f"AfriLabel QA Studio: {report['status']}")
    print(f"Images checked: {report['images_checked']}")
    print(f"Annotations checked: {report['annotations_checked']}")
    print(f"Errors: {report['error_count']} | Warnings: {report['warning_count']}")
    print(f"Reports saved to: {args.output.resolve()}")

    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
