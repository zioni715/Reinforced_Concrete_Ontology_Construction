from __future__ import annotations

import csv
import json
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = Path(__file__).resolve().parent
MODELS_MANIFEST = EXPERIMENT_DIR / "models" / "model_manifest.json"
ANSWER_KEY = EXPERIMENT_DIR / "evaluation" / "model_capability_answer_key.json"
QUERY_DIR = EXPERIMENT_DIR / "evaluation" / "model_capability_sparql"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_graph(files: list[str]) -> Graph:
    graph = Graph()
    for file_name in files:
        graph.parse(ROOT / file_name, format="turtle")
    return graph


def run_ask_query(graph: Graph, query_path: Path) -> bool:
    result = graph.query(query_path.read_text(encoding="utf-8"))
    if result.type != "ASK":
        raise ValueError(f"{query_path.name} must be an ASK query")
    return bool(result.askAnswer)


def main() -> None:
    manifest = load_json(MODELS_MANIFEST)
    answer_key = load_json(ANSWER_KEY)
    base_files = manifest["base_data_files"]
    query_specs = answer_key["queries"]

    max_points = sum(float(spec["weight"]) for spec in query_specs)
    result_rows: list[dict] = []
    score_rows: list[dict] = []
    criterion_rows: list[dict] = []
    detail_payload = {
        "experiment_id": manifest["experiment_id"],
        "base_data_files": base_files,
        "answer_key": str(ANSWER_KEY.relative_to(ROOT)),
        "query_directory": str(QUERY_DIR.relative_to(ROOT)),
        "max_points": max_points,
        "models": [],
    }

    for model in manifest["combinations"]:
        model_files = base_files + model["extension_files"]
        graph = load_graph(model_files)
        model_points = 0.0
        key_matches = 0
        criterion_totals: dict[str, dict[str, float]] = {}
        model_query_results = []

        for spec in query_specs:
            query_path = QUERY_DIR / spec["file"]
            actual = run_ask_query(graph, query_path)
            expected = model["id"] in spec["expected_true_models"]
            answer_key_match = actual == expected
            points = float(spec["weight"]) if actual else 0.0

            if answer_key_match:
                key_matches += 1
            model_points += points

            criterion = spec["criterion"]
            criterion_totals.setdefault(criterion, {"earned": 0.0, "possible": 0.0})
            criterion_totals[criterion]["possible"] += float(spec["weight"])
            criterion_totals[criterion]["earned"] += points

            row = {
                "model_id": model["id"],
                "model_label": model["label"],
                "query_id": spec["id"],
                "query_file": spec["file"],
                "criterion": criterion,
                "weight": spec["weight"],
                "expected": str(expected).lower(),
                "actual": str(actual).lower(),
                "answer_key_match": str(answer_key_match).lower(),
            }
            result_rows.append(row)
            model_query_results.append({**row, "question": spec["question"]})

        normalized_score = round((model_points / max_points) * 100, 2)
        score_rows.append({
            "model_id": model["id"],
            "model_label": model["label"],
            "graph_triples": len(graph),
            "capability_points": round(model_points, 2),
            "max_points": round(max_points, 2),
            "normalized_score": normalized_score,
            "answer_key_matches": key_matches,
            "query_count": len(query_specs),
        })

        for criterion, values in sorted(criterion_totals.items()):
            earned = values["earned"]
            possible = values["possible"]
            criterion_rows.append({
                "model_id": model["id"],
                "model_label": model["label"],
                "criterion": criterion,
                "earned_points": round(earned, 2),
                "possible_points": round(possible, 2),
                "criterion_score": round((earned / possible) * 100, 2) if possible else 0.0,
            })

        detail_payload["models"].append({
            "model_id": model["id"],
            "model_label": model["label"],
            "data_files": model_files,
            "graph_triples": len(graph),
            "capability_points": round(model_points, 2),
            "normalized_score": normalized_score,
            "answer_key_matches": key_matches,
            "query_count": len(query_specs),
            "queries": model_query_results,
        })

    score_rows.sort(key=lambda row: row["capability_points"], reverse=True)
    for rank, row in enumerate(score_rows, start=1):
        row["rank"] = rank

    for model_detail in detail_payload["models"]:
        rank_row = next(row for row in score_rows if row["model_id"] == model_detail["model_id"])
        model_detail["rank"] = rank_row["rank"]

    result_csv = EXPERIMENT_DIR / "model_capability_results.csv"
    with result_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "model_id",
                "model_label",
                "query_id",
                "query_file",
                "criterion",
                "weight",
                "expected",
                "actual",
                "answer_key_match",
            ],
        )
        writer.writeheader()
        writer.writerows(result_rows)

    score_csv = EXPERIMENT_DIR / "model_capability_scores.csv"
    with score_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "rank",
                "model_id",
                "model_label",
                "graph_triples",
                "capability_points",
                "max_points",
                "normalized_score",
                "answer_key_matches",
                "query_count",
            ],
        )
        writer.writeheader()
        writer.writerows(score_rows)

    criterion_csv = EXPERIMENT_DIR / "model_capability_criterion_scores.csv"
    with criterion_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "model_id",
                "model_label",
                "criterion",
                "earned_points",
                "possible_points",
                "criterion_score",
            ],
        )
        writer.writeheader()
        writer.writerows(criterion_rows)

    detail_json = EXPERIMENT_DIR / "model_capability_results.json"
    detail_json.write_text(
        json.dumps(detail_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    all_key_matches = sum(1 for row in result_rows if row["answer_key_match"] == "true")
    print(f"models={len(manifest['combinations'])}")
    print(f"queries={len(query_specs)}")
    print(f"model_query_pairs={len(result_rows)}")
    print(f"answer_key_matches={all_key_matches}")
    print(f"answer_key_mismatches={len(result_rows) - all_key_matches}")
    print(f"winner={score_rows[0]['model_label']}")
    print(f"winner_score={score_rows[0]['capability_points']}/{score_rows[0]['max_points']}")


if __name__ == "__main__":
    main()
