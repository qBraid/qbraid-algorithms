"""Base class for quantum dynamics implementations."""

from abc import ABC, abstractmethod
from typing import Optional, Union

import numpy as np


class DynamicsBase(ABC):
    """Abstract base class for quantum dynamics implementations.
    
    This class defines the interface that all quantum dynamics classes must implement.
    It provides a standard way to evolve quantum states according to different 
    evolution schemes (Magnus expansion, analog evolution, etc.).
    """

    def __init__(self, num_sites: int, **kwargs):
        """Initialize dynamics parameters.
        
        Args:
            num_sites: Number of sites in the quantum system
            **kwargs: Additional parameters specific to the dynamics implementation
        """
        self.num_sites = num_sites
        self._validate_parameters(**kwargs)
        
    @abstractmethod
    def evolve(
        self, 
        initial_state: np.ndarray,
        time: Union[float, np.ndarray],
        backend: Optional[str] = None
    ) -> np.ndarray:
        """Evolve the quantum state according to the dynamics.
        
        Args:
            initial_state: Initial quantum state
            time: Evolution time(s)
            backend: Optional backend specification for computation
            
        Returns:
            Evolved quantum state
        """
        pass
    
    @abstractmethod
    def _validate_parameters(self, **kwargs) -> None:
        """Validate the parameters passed to the dynamics implementation."""
        pass
    
    def reset(self) -> None:
        """Reset any internal state of the dynamics."""
        pass