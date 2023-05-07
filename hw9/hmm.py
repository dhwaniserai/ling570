from collections import defaultdict
from math import log10


def check_template(line):
    if (
        (line[:10] == "state_num=")
        or (line[:8] == "sym_num=")
        or (line[:14] == "init_line_num=")
        or (line[:15] == "trans_line_num=")
        or (line[:15] == "emiss_line_num=")
    ):
        return line.split("=")
    else:
        return None


def check_probability(num, line_num):
    if 1 >= num > 0:
        return True
    elif num == 0:
        return False
    else:
        print("warning: the prob is not in [0,1] range:{}".format(line_num), sys.stderr)
        return False


class HMM:
    def __init__(self, lines):
        # initialize sections
        self.template_section = True
        self.init_section = False
        self.transition_section = False
        self.emission_section = False
        # intialize variables
        self.prob_init = {}
        self.transitions = defaultdict(dict)
        self.emissions = defaultdict(dict)
        # template hmm params from file header
        self.hmm_params_template = {
            "state_num": 0,
            "sym_num": 0,
            "init_line_num": 0,
            "trans_line_num": 0,
            "emiss_line_num": 0,
        }
        # true hmm params
        self.hmm_params = {
            "state_num": 0,
            "sym_num": 0,
            "init_line_num": 0,
            "trans_line_num": 0,
            "emiss_line_num": 0,
        }
        self.process_sections(lines)
        self.true_states, self.vocab = self.get_true_states()
        self.print_hmm_stats()

    def process_template_section(self, line):
        if self.template_section:
            flag = check_template(line=line)
            if flag:
                self.hmm_params_template[flag[0]] = int(flag[1])
            else:
                self.template_section = False

    def process_non_template_section(self, line):
        #check if all sections exist in the file
        emission = False
        transition = False
        init = False
        if line == "\\init":
            init = True
        elif line == "\\transition":
            transition = True
        elif line == "\\emission":
            emission = True
        self.emission_section = emission
        self.transition_section = transition
        self.init_section = init

    def handle_init_section(self, line, ind):
        source = line.split()[0]
        prob = float(line.split()[1])
        if check_probability(prob, ind):
            try:
                log_prob = float(line.split()[2])
            except IndexError:
                log_prob = log10(prob)
            self.prob_init[source] = log_prob
        self.hmm_params["init_line_num"] += 1

    def handle_transition_section(self, line, ind):
        source = line.split()[0]
        target = line.split()[1]
        prob = float(line.split()[2])
        if target in self.transitions[source]:
            print(
                "warning: malformed HMM file. repeated transition %s to %s. original_prob: %.10f new_prob: %.10f"
                % (
                    source,
                    target,
                    self.transitions[source][target],
                    prob,
                ),
                file=sys.stderr,
            )
        elif check_probability(prob, ind):
            try:
                log_prob = float(line.split()[3])
            except IndexError:
                log_prob = log10(prob)
            self.transitions[source][target] = log_prob
        self.hmm_params["trans_line_num"] += 1

    def handle_emission_section(self, line, ind):
        source = line.split()[0]
        sym = line.split()[1]
        prob = float(line.split()[2])
        if sym in self.emissions[source]:
            print(
                "warning: malformed HMM file. repeated emission %s to %s. original_prob: %.10f new_prob: %.10f"
                % (source, sym, self.emissions[source][sym], prob),
                file=sys.stderr,
            )
        elif check_probability(prob, ind):
            try:
                log_prob = float(line.split()[3])
            except IndexError:
                log_prob = log10(prob)
            self.emissions[source][sym] = log_prob
        self.hmm_params["emiss_line_num"] += 1

    def process_sections(self, lines):
        for ind, line in enumerate(lines):
            self.process_template_section(line)
            if not self.template_section:
                if line in ["\\init", "\\transition", "\\emission"]:
                    self.process_non_template_section(line)
                else:
                    if self.init_section:
                        self.handle_init_section(line, ind)
                    elif self.transition_section:
                        self.handle_transition_section(line, ind)
                    elif self.emission_section:
                        self.handle_emission_section(line, ind)

    def get_true_states(self):
        # to get actual states in hmm
        init_states = set(self.prob_init.keys())
        transition_source_states = set(self.transitions.keys())
        transition_target_states = set([t for s in self.transitions for t in self.transitions[s]])
        emissions_states = set(self.emissions.keys())
        true_states = (
            init_states.union(transition_source_states)
            .union(transition_target_states)
            .union(emissions_states)
        )
        self.hmm_params["state_num"] = len(true_states)
        # get true symbols
        true_syms = set(
            [sym for state in self.emissions for sym in self.emissions[state]]
        )
        self.hmm_params["sym_num"] = len(true_syms)
        return true_states, true_syms

    def print_hmm_stats(self):
        print("HMM statistics")
        for param in [
            "state_num",
            "sym_num",
            "init_line_num",
            "trans_line_num",
            "emiss_line_num",
        ]:
            print(
                "Param:{}\tDump:{}\tActual:{}".format(
                    param,
                    self.hmm_params_template.get(param, "NULL"),
                    self.hmm_params.get(param, "NULL"),
                )
            )
