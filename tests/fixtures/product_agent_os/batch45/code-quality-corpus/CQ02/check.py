import importlib.util,sys
p=sys.argv[1]
s=importlib.util.spec_from_file_location('candidate',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class Item:
    comparisons=0
    def __init__(self, value): self.value=value
    def __hash__(self): return hash(self.value)
    def __eq__(self, other):
        Item.comparisons+=1
        return self.value==other.value
assert m.unique([3,1,3,2])==[3,1,2]
assert len(m.unique([Item(i) for i in range(100)]))==100
assert Item.comparisons < 500, 'quadratic equality work'

