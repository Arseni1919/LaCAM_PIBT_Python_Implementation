from globals import *


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# CLASSES
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCS
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def get_sorted_nei_nodes(
        agent: AgentAlg,
        config_from: Dict[str, Node],
        nodes_dict: Dict[str, Node],
        h_dict: Dict[str, np.ndarray],
):
    h_goal_np: np.ndarray = h_dict[agent.goal_node.xy_name]
    # sort C in ascending order of dist(u, gi) where u ∈ C
    nei_nodes: List[Node] = [nodes_dict[n_name] for n_name in config_from[agent.name].neighbours]
    random.shuffle(nei_nodes)

    def get_nei_v(n: Node) -> float:
        return float(h_goal_np[n.x, n.y])

    nei_nodes.sort(key=get_nei_v)
    return nei_nodes


def there_is_vc(
        nei_node: Node,
        config_to: Dict[str, Node],
) -> bool:
    for name, n in config_to.items():
        if nei_node == n:
            return True
    return False


def get_agent_k(
        nei_node: Node,
        config_from: Dict[str, Node],
        config_to: Dict[str, Node],
        agents_dict: Dict[str, AgentAlg],
) -> AgentAlg | None:
    for a_f_name, n_f_node in config_from.items():
        if n_f_node == nei_node and a_f_name not in config_to:
            return agents_dict[a_f_name]
    return None


def there_is_ec(
        agent_i: AgentAlg,
        node_to: Node,
        config_from: Dict[str, Node],
        config_to: Dict[str, Node],
) -> bool:
    node_from = config_from[agent_i.name]
    for other_name, other_node_from in config_from.items():
        if other_name == agent_i.name or other_name not in config_to:
            continue
        other_node_to = config_to[other_name]
        if other_node_from == node_to and other_node_to == node_from:
            return True
    return False











