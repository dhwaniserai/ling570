from argparse import ArgumentParser
from hmm import HMM #check hmm files from last time
from trellis import TrellisEntry, backtrace_trellis, get_current_trellis_col


def read_file(filename):
    with open(filename, "r") as f:
        lines = [x.strip() for x in f.readlines() if x.strip()]
    return lines


def write_output(file, lines):
    with open(file, "w") as f:
        for line in lines:
            f.write(line)


class ViterbiDecoder:
    def __init__(self, hmm, lines):
        self.hmm = hmm
        self.output = self.decode_lines(lines)

    def decode_lines(self, lines):
        # decoding each line using the viterbi_decode function to get output in proper format
        output = []
        for line in lines:
            observations = line.split()
            path, final_log_prob = self.viterbi_decode(observations)
            output.append(
                "{} => {} {}\n".format(
                    " ".join(observations), " ".join(path), final_log_prob
                )
            )
        return output

    def viterbi_decode(self, observations):
        trellis = [{}]
        # Initializing first state in trellis
        for init_state in self.hmm.prob_init:
            init_log_prob = self.hmm.prob_init[init_state]
            trellis[0][init_state] = TrellisEntry(
                log_prob=init_log_prob, back_pointer=None
            )
        # Induction
        for t in range(1, len(observations) + 1):
            obs = observations[t - 1]
            
            if obs not in self.hmm.vocab: # OOV Handling
                obs = "<unk>" 
            curr_col = get_current_trellis_col(
                trellis[-1], #previous column
                obs, #current observation
                self.hmm.transitions,
                self.hmm.emissions,
            )
            trellis.append(curr_col)
        # Backtrace
        path, final_log_prob = backtrace_trellis(trellis)
        return path, final_log_prob


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--input_hmm", type=str, required=True)
    arg_parser.add_argument("--test_file", type=str, required=True)
    arg_parser.add_argument("--output", type=str, required=True)
    args = arg_parser.parse_args()

    hmm_lines = read_file(args.input_hmm)
    test_lines = read_file(args.test_file)
    hmm = HMM(hmm_lines)
    decoded_test = ViterbiDecoder(hmm, test_lines)
    write_output(args.output_file, decoded_test.output)


