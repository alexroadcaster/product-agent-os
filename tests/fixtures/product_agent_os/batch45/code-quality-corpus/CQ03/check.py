import importlib.util,sys
p=sys.argv[1]
s=importlib.util.spec_from_file_location('candidate',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
assert m.allowed(18); assert not m.allowed(17); assert m.allowed(19)
