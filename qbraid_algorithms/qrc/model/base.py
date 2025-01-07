"""Base class for quantum reservoir computing models."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import numpy as np

from ..dynamics.base import DynamicsBase
from ..encoding.base import EncoderBase


class QRCModelBase(ABC):
    """Abstract base class for quantum reservoir computing models.
    
    This class combines encoding and dynamics components to create a complete
    quantum reservoir computing model.
    """
    
    def __init__(
        self,
        encoder: EncoderBase,
        dynamics: DynamicsBase,
        random_state: Optional[int] = None
    ):
        """Initialize the QRC model.
        
        Args:
            encoder: Encoder for transforming classical data
            dynamics: Quantum dynamics implementation
            random_state: Random seed for reproducibility
        """
        self.encoder = encoder
        self.dynamics = dynamics
        self._set_random_state(random_state)
        
    @abstractmethod
    def fit(
        self, 
        X: np.ndarray, 
        y: np.ndarray,
        **kwargs
    ) -> "QRCModelBase":
        """Train the model on given data.
        
        Args:
            X: Training input data
            y: Training target values
            **kwargs: Additional training parameters
            
        Returns:
            self: The trained model
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            X: Input data for prediction
            
        Returns:
            Model predictions
        """
        pass
    
    def _set_random_state(self, random_state: Optional[int]) -> None:
        """Set random state for reproducibility."""
        if random_state is not None:
            np.random.seed(random_state)