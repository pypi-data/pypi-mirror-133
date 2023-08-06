import os, json, math

def save_file(name: str, _data: dict):
    with open(name, mode = "w", encoding= "utf-8") as f: json.dump(_data, f)

def load_file(name) -> dict:
    if not os.path.isfile(name):
        raise FileNotFoundError(f"File '{name}' Not Found")
    with open(name, mode = "r", encoding = "utf-8") as f: return json.load(f)

def make_line(x1: int, y1: int, x2: int, y2: int):
    def dist(xs, ys):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(xs, ys)))

    def get_heading(xy_a,xy_b):
        x,y = xy_b[0]-xy_a[0], xy_b[1]-xy_a[1]
        return (math.atan2(x,y)*180/math.pi) % 360

    def get_unit_vector(heading):
        r = math.radians(heading)
        return math.sin(r), math.cos(r)


    start = (x1, y1)

    end = (x2, y2)

    unit_vector = get_unit_vector(get_heading(start,end))
    dist = dist(start, end)
    points = []
    for i in range(int(dist)):
        new_point = int(start[0]+(unit_vector[0]*i)), int(start[1]+(unit_vector[1]*i))
        if new_point not in points:
            points.append(new_point)
    points.append(end)
    return points