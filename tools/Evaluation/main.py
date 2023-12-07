from Evaluation import evaluate_dataset, read_scores_from_json

if __name__ == "__main__":
    json_file_path = "../../data/files/EvaluationData/Results/Untrained_DK.json"

    scores = read_scores_from_json(json_file_path)
    evaluate_dataset(scores)
