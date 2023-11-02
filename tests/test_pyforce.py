import pytest
from pyforce import pyforce


class TestPyforce():
    
    
    def setup(self) -> None:    
        self.pyforce = pyforce.Pyforce(trellis_devint_config)
    
    
    def test_init_with_config(self) -> None:
        assert pyforce is not None
        assert self.pyforce is not None
        assert self.pyforce.sfinstance is not None
        
    
    def test_get_contacts(self):
    
        limits = [-1, 0, 1, 5, 15]

        for l in limits:
            contacts = self.pyforce.get_contacts(limit=l)
            if l < 0:
                assert len(contacts) == 0
            else:
                assert len(contacts) == l
