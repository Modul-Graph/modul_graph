# this class is necessary to pass the 'standard_curriculum' parameter (controller input from frontend) to repository

class StdCurr:
    name: str


std_curr: StdCurr = StdCurr()


def instantiate_std_curr_obj(name: str):
    global std_curr
    std_curr.name = name