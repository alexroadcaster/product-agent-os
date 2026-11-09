import importlib.util,sys
p=sys.argv[1]
s=importlib.util.spec_from_file_location('candidate',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
assert m.timeout(0)==0; assert m.timeout(None)==30; assert m.timeout(8)==8
