
class AppendEntryRequest(object):
    def __init__(term, leader, previous_log_index, previous_log_term, entry_key, entry_value, leader_commit_index):
        self.term = term
        self.leader = leader
        self.previous_log_index = previous_log_index
        self.previous_log_term = previous_log_term
        self.entry_key = entry_key
        self.entry_value = entry_value
        self.leader_commit_index = leader_commit_index


class AppendEntryResponse(object):
    def __init__(self, term, success):
        self.term = term
        self.success = success


class RequestVoteRequest(object):
    def __init__(self, term, candidate, last_log_index, last_log_term):
        self.term = term
        self.candidate = candidate
        self.last_log_index = last_log_index
        self.last_log_term = last_log_term


class RequestVoteResponse(object):
    def __init__(self, term, vote_granted):
        self.term = term
        self.vote_granted = vote_granted
