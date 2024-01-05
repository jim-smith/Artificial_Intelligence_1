from problem import Problem

Debug = False


class FoxChickenGrain(Problem):
    """Class for the fox-chicken-grain problem."""

    def __init__(self):
        self.value_set = [0, 1, 2, 3, 4, 5, 6, 7]
        self.move_names = [
            "b_01",
            "bg_01",
            "bc_01",
            "bf_01",
            "b_10",
            "bg_10",
            "bc_10",
            "bf_10",
        ]

    def evaluate(self, attempt: list) -> tuple[int, str]:
        # runs through the moves stopping as soon as there is a problem
        # all start on bank 0
        locations: dict = {"fox": 0, "chicken": 0, "grain": 0, "boat": 0}

        for next_move in attempt:
            ok, location_reason = self.things_in_right_place(locations, next_move)
            if not ok:
                pass
                # this version ignores moves that can't be made when decoding solution
                # uncomment line below to say those solutions are invalid
                # return -1, location_reason

            else:  # move things
                next_bank = 1 if next_move < 4 else 0
                locations["boat"] = next_bank
                if next_move in [1, 5]:
                    locations["grain"] = next_bank
                if next_move in [2, 6]:
                    locations["chicken"] = next_bank
                if next_move in [3, 7]:
                    locations["fox"] = next_bank

            # does valid partial solution break the constraints?
            if locations["boat"] != locations["chicken"]:
                if locations["chicken"] == locations["fox"]:
                    return -1, "fox eats chicken"

                if locations["chicken"] == locations["grain"]:
                    return -1, "chicken eats grain"

            # check for goal
            if list(locations.values()) == [1, 1, 1, 1]:
                return 1, "goal reached"

        # got to end without breaking cionstraints or reaching goal
        return 0, ""

    def display(self, attempt: list) -> str:
        """Outputs a candidate solution as a series of moves.""" ""
        len(attempt)
        movelist = ""
        for move in attempt:
            movelist = movelist + "->" + self.move_names[move]
        return movelist

    def things_in_right_place(self, locations: dict, move: int) -> tuple[bool, str]:
        """Checks whether things are in the right place for the proposed move."""

        ok = True
        reason = ""
        pair_to_move = move % 4
        leaving_bank = move // 4
        if Debug:
            print(
                f" move {move} pair {pair_to_move} "
                f"leaving {leaving_bank} "
                f"locations {locations}"
            )
        # boat always has to be in right place
        if leaving_bank != locations["boat"]:
            reason = "boat is in wrong place "
            ok = False

        # grain moving as well
        elif pair_to_move == 1 and leaving_bank != locations["grain"]:
            ok = False
            reason += "grain is in wrong place"

        # chicken moving as well
        elif pair_to_move == 2 and leaving_bank != locations["chicken"]:
            ok = False
            reason += "chicken is in wrong place"

        # fox moving as well
        elif pair_to_move == 3 and leaving_bank != locations["fox"]:
            ok = False
            reason += "fox is in wrong place"

        return ok, reason
