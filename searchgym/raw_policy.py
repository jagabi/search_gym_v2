"""Effective policy metadata shared by CLI, saved configuration and runtime traces."""


def raw_policy(config, method):
    if method != "jevtree" or config.jev_strategy != "raw":
        return None
    progressive = config.jev_traversal == "progressive"
    return {
        "traversal": config.jev_traversal,
        "expected_traversal": config.jev_expected_traversal or None,
        "tools": ["web_search", "read_source", "continue_search"] if progressive else ["web_search"],
        "research_state": progressive,
        "final_evidence_review": progressive or config.finalize_answer,
        "http_wave": {"requests": config.jev_concurrency, "questions_per_request": config.jev_packet_questions,
                      "question_budget": config.jev_inflight_questions, "wait_for_all": True},
        "max_searches": config.max_searches,
        "initial_pages": config.jev_entries,
        "visits_per_search_limit": config.jev_fetch_budget,
        "visits_per_continue": config.jev_expand_batch,
        "parents_per_action_limit": config.jev_parent_limit if progressive else None,
        "read_quotas": [config.jev_direct_reads, config.jev_query_reads],
        "question_targets_not_limits": {"visits": config.jev_target_visits,
            "reads": config.jev_target_reads, "parent_expansions": config.jev_target_expansions} if progressive else None,
    }
