from esmerald import Include

route_patterns = [
    Include(namespace="banking.bank.apps.v1.urls", name="bank", path="/v1"),
]