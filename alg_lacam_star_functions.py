from globals import *
from alg_pibt import run_procedure_pibt
# from alg_lacam_funcitons import *


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# CLASSES
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class LowLevelNodeStar:
    def __init__(self,
                 parent: Self | None,
                 who: AgentAlg | None,
                 where: Node | None,
                 depth: int):
        self.parent: Self | None = parent
        self.who: AgentAlg | None = who
        self.where: Node | None = where
        self.depth = depth
        self.who_list: List[AgentAlg] = []
        self.where_list: List[Node] = []


class HighLevelNodeStar:
    def __init__(
            self,
            config: Dict[str, Node],
            tree: Deque[LowLevelNodeStar],
            order: List[AgentAlg],
            parent: Self | None,
            g: int = 0,
            h: int = 0,
            finished: int = 0,
    ):
        self.config: Dict[str, Node] = config
        self.tree: Deque[LowLevelNodeStar] = tree
        self.order: List[AgentAlg] = order
        self.parent: Self | None = parent
        self.finished: int = finished
        self.name = get_config_name(self.config)
        self.g: int = g
        self.h: int = h
        self.f: int = self.g + self.h
        self.neigh: Set[Self] = set()

    def __eq__(self, other: Self):
        return self.name == other.name

    def __str__(self):
        return self.name

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# HELP FUNCS
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def get_C_init():
    return LowLevelNodeStar(None, None, None, 0)


def get_C_child(
        parent: LowLevelNodeStar,
        who: AgentAlg,
        where: Node
) -> LowLevelNodeStar:
    C_new = LowLevelNodeStar(parent=parent, who=who, where=where, depth=parent.depth + 1)
    C_new.who_list = parent.who_list + [who]
    C_new.where_list = parent.where_list + [where]
    return C_new


def get_init_order(
        agents: List[AgentAlg],
        config: Dict[str, Node],
        h_dict: Dict[str, np.ndarray]
) -> List[AgentAlg]:
    def get_h_value(a: AgentAlg) -> float:
        curr_node = config[a.name]
        h_map = h_dict[a.goal_node.xy_name]
        res: float = float(h_map[curr_node.x, curr_node.y])
        return res
    out_list: List[AgentAlg] = agents[:]
    out_list.sort(key=get_h_value, reverse=True)
    return out_list


def get_order(
        config_new: Dict[str, Node],
        N: HighLevelNodeStar
) -> Tuple[List[AgentAlg], int]:
    finished: List[AgentAlg] = []
    unfinished: List[AgentAlg] = []
    for a in N.order:
        if config_new[a.name] == a.goal_node:
            finished.append(a)
        else:
            unfinished.append(a)
    return [*unfinished, *finished], len(finished)


def get_config_name(config: Dict[str, Node]):
    assert len(config) > 0
    k_list = list(config.keys())
    k_list.sort()
    name = ''
    for k in k_list:
        v = config[k]
        name += v.xy_name + '-'
    return name[:-1]


def backtrack(N: HighLevelNodeStar) -> Dict[str, List[Node]]:
    paths_deque_dict: Dict[str, Deque[Node]] = {k: deque([v]) for k, v in N.config.items()}
    parent: HighLevelNodeStar = N.parent
    while parent is not None:
        for k, v in parent.config.items():
            paths_deque_dict[k].appendleft(v)
        parent = parent.parent

    paths_dict: Dict[str, List[Node]] = {}
    for k, v in paths_deque_dict.items():
        paths_dict[k] = list(v)

    return paths_dict


def get_new_config(
        N: HighLevelNodeStar,
        C: LowLevelNodeStar,
        agents_dict: Dict[str, AgentAlg],
        nodes_dict: Dict[str, Node],
        h_dict: Dict[str, np.ndarray],
) -> Dict[str, Node] | None:
    # setup next configuration
    config_from: Dict[str, Node] = N.config
    config_to: Dict[str, Node] = {}
    for k in range(C.depth):
        config_to[C.who_list[k].name] = C.where_list[k]

    # apply PIBT
    for agent in N.order:
        if agent.name not in config_to:
            success = run_procedure_pibt(agent, None, config_from, config_to, agents_dict, nodes_dict, h_dict, [])
            if not success:
                return None
    return config_to




