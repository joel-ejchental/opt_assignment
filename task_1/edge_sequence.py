import os
import xml.etree.ElementTree as ET

def edge_connection(con_data):
    edge_neighbors = {}
    for conn in con_data.findall('connection'):
        source = conn.get('from')
        dest = conn.get('to')
        if source not in edge_neighbors:
            edge_neighbors[source] = [dest]
        else:
            if dest not in edge_neighbors[source]:
                edge_neighbors[source].append(dest)
    return edge_neighbors

def find_root_edges(edge_neighbors):
    sources = set(edge_neighbors.keys())
    dests = {dest for dest_list in edge_neighbors.values() for dest in dest_list}
    root_edge = sources - dests
    return root_edge
    

def extend_routes(edge_neighbors, roots):
    edge_sequence = []

    for source_edge in roots:
        source_paths = [[source_edge]]
        finished_path = []

        while source_paths:
            current_edge_path = source_paths.pop(0)
            farthest_edge = current_edge_path[-1]
            if farthest_edge is None:
                finished_path.append(current_edge_path[:-1])
                continue

            next_edges = edge_neighbors.get(farthest_edge)
            if not next_edges:
                finished_path.append(current_edge_path)
            else:
                for next_edge in next_edges:
                    source_paths.append(current_edge_path + [next_edge])

        edge_sequence.extend(finished_path)

    return edge_sequence


def print_edge_sequences(edge_sequence):
    for path in edge_sequence:
        print(" -> ".join(path))


def verify(edge_neighbors, edge_sequence):
    for route in edge_sequence:
        for i in range(len(route) - 1):
            current_edge = route[i]
            next_edge = route[i + 1]
            if next_edge not in edge_neighbors.get(current_edge):
                print(f"faulty route: {route}")
                break
    print('\nAll routes verified')


def read_file(filename):
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    sumu_dir = os.path.join(parent_dir, 'sumu_files')
    file_path = os.path.join(sumu_dir, filename)

    file_parsed = ET.parse(file_path)
    data = file_parsed.getroot()
    return data



if __name__ == '__main__':

    con_data = read_file('test.con.xml')
    edge_neighbors = edge_connection(con_data)
    root_edge = find_root_edges(edge_neighbors)
    edge_sequence = extend_routes(edge_neighbors, root_edge)
    print_edge_sequences(edge_sequence)
    verify(edge_neighbors, edge_sequence)
