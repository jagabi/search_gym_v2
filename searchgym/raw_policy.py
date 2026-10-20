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
        "entry_candidates": config.jev_entry_candidates if config.jev_rank_entries else None,
        "entry_selection": "d3" if config.jev_rank_entries else "search_order",
        "visits_per_search_limit": config.jev_fetch_budget,
        "visits_per_continue": config.jev_expand_batch if progressive else None,
        "parents_per_action_limit": config.jev_parent_limit if progressive else None,
        "read_quotas": [config.jev_direct_reads, config.jev_query_reads],
        "complementary_reads": config.jev_diverse_reads,
        "complementary_read_context": "selected_evidence_chunks" if config.jev_diverse_reads and not progressive else None,
        "link_parent_beam": config.jev_frontier_width if not progressive and config.jev_traversal == 'beam' else None,
        "link_expansion": "missing_relation_then_links" if not progressive else "progressive",
        "read_dedup": config.jev_read_dedup,
        "navigation_notice_tokens": config.jev_notice_tokens,
        "document_routing": {"selector": "d3", "min_bundles": config.jev_tree_min_bundles,
            "branch": config.jev_region_branch, "beam": config.jev_region_beam,
            "preview_tokens": config.jev_region_tokens,
            "leaf_bundles": config.jev_leaf_bundles} if config.jev_document_tree else None,
        "question_targets_not_limits": {"visits": config.jev_target_visits,
            "reads": config.jev_target_reads, "parent_expansions": config.jev_target_expansions} if progressive else None,
    }
