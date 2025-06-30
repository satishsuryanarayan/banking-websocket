from esmerald import Include

route_patterns = [
    Include(namespace="bank.v1.urls", name="bank", path="/v1"),
]