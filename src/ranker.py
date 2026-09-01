def rank_candidates(candidates):
    """
    Rank candidates by their final score
    in descending order.
    """

    ranked_candidates = sorted(
        candidates,
        key=lambda candidate: candidate["final_score"],
        reverse=True
    )

    for rank, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = rank

    return ranked_candidates