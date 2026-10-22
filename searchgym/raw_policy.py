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
        "decision_batching": {"scope": "same_search_phase_runnable_items",
                              "source_token_budget": config.jev_bundle_tokens,
                              "source_binding": "shared_plus_per_item_original_state",
                              "partial_results": "preserve_valid_keys"},
        "max_searches": config.max_searches,
        "initial_pages": config.jev_entries,
        "entry_candidates": config.jev_entry_candidates if config.jev_rank_entries else None,
        "entry_selection": "d3" if config.jev_rank_entries else "search_order",
        "entry_complement_slots": min(config.jev_frontier_width,
            min(config.jev_entries, config.jev_fetch_budget)-1) if config.jev_rank_entries and
            config.jev_traversal == 'beam' and min(config.jev_entries, config.jev_fetch_budget) >= 3 else 0,
        "visits_per_search_limit": config.jev_fetch_budget,
        "visits_per_continue": config.jev_expand_batch if progressive else None,
        "parents_per_action_limit": config.jev_parent_limit if progressive else None,
        "read_quotas": [config.jev_direct_reads, config.jev_query_reads],
        "complementary_reads": config.jev_diverse_reads,
        "complementary_read_context": "selected_evidence_chunks" if not progressive and (config.jev_diverse_reads or config.jev_traversal == 'beam') else None,
        "link_parent_beam": config.jev_frontier_width if not progressive and config.jev_traversal == 'beam' else None,
        "link_expansion": ("node_action_then_links" if config.jev_traversal == 'beam' else
                           "progressive" if progressive else "missing_relation_then_links"),
        "branch_control": {"actions": ["return_now", "read_now", "expand_now"],
                           "selection": "eligible_read_expand_then_close", "depth_barrier": True,
                           "read_floor": config.jev_floor,
                           "expand_floor": config.jev_link_floor,
                           "read_before_next_depth": True,
                           "sibling_action_order": "higher_expand_before_lower_read",
                           "last_read": "explicit_terminal_choice",
                           "route_observation": "prefix_urls_and_selected_original_chunks",
                           "read_value": "expected_full_document_gain_available_objectives",
                           "return_value": "no_eligible_operation_no_separate_judgment",
                           "reading_pool": "current_depth_scored_documents",
                           "zero_read_selection": "no_forced_read_below_floor"} if config.jev_traversal == 'beam' else None,
        "evidence_first": config.jev_traversal == 'beam',
        "read_dedup": config.jev_read_dedup,
        "navigation_notice_tokens": config.jev_notice_tokens,
        "document_routing": {"selector": "d3", "min_bundles": config.jev_tree_min_bundles,
            "branch": config.jev_region_branch, "beam": config.jev_region_beam,
            "preview_tokens": config.jev_region_tokens,
            "leaf_bundles": config.jev_leaf_bundles} if config.jev_document_tree else None,
        "question_targets_not_limits": {"visits": config.jev_target_visits,
            "reads": config.jev_target_reads, "parent_expansions": config.jev_target_expansions} if progressive else None,
    }
