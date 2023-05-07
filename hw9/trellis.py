class TrellisEntry:
    def __init__(self, log_prob, back_pointer):
        self.log_prob = log_prob
        self.back_pointer = back_pointer


def backtrace_trellis(trellis):
    #viterbi bactracking function to get appropriate states producing the observations

    path = []
    # Final state
    final_entry = max(trellis[-1].items(), key=lambda x: x[1].log_prob)
    final_state = final_entry[0]
    final_lg_prob = final_entry[1].log_prob
    prev_state = final_entry[1].back_pointer
    path.append(final_state)
    # Backpointer to trace trellis
    for i in range(len(trellis) - 2, -1, -1):
        path.append(prev_state)
        prev_state = trellis[i][prev_state].back_pointer
    path.reverse()
    return path, final_lg_prob


def get_current_trellis_col(previous_column, observation, transitions, emissions):
    current_column = {}
    for source_state in previous_column:
        try:
            for target_state in transitions[source_state]:
                try:
                    if observation in emissions[target_state]:
                        transition_log_prob = transitions[source_state][target_state]
                        emission_log_prob = emissions[target_state][observation]
                        entry_log_prob = (
                            previous_column[source_state].log_prob
                            + transition_log_prob
                            + emission_log_prob
                        )
                        entry_back_pointer = source_state
                        if target_state in current_column:
                            if current_column[target_state].log_prob < entry_log_prob:
                                current_column[target_state] = TrellisEntry(
                                    log_prob=entry_log_prob,
                                    back_pointer=entry_back_pointer,
                                )
                        else:
                            current_column[target_state] = TrellisEntry(
                                log_prob=entry_log_prob, back_pointer=entry_back_pointer
                            )
                except KeyError: # if key is not there just skip it
                    continue
        except KeyError:
            continue
    return current_column
