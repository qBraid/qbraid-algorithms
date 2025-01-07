"""Base class for encoding classical data into quantum states."""

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class EncoderBase(ABC):
    """Abstract base class for encoding classical data into quantum states.
    
    This class defines the interface for transforming classical data into a format
    suitable for quantum evolution, with methods for both encoding and decoding.
    """
    
    def __init__(self, input_dim: int, output_dim: int, **kwargs):
        """Initialize encoder parameters.
        
        Args:
            input_dim: Dimension of input classical data
            output_dim: Dimension of encoded quantum data
            **kwargs: Additional parameters specific to the encoding method
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self._validate_dimensions()
        
    @abstractmethod
    def encode(self, data: np.ndarray, normalize: bool = True) -> np.ndarray:
        """Transform classical data into quantum encoding.
        
        Args:
            data: Classical data to encode
            normalize: Whether to normalize the encoded data
            
        Returns:
            Encoded quantum data
        """
        pass
    
    @abstractmethod
    def decode(self, encoded_data: np.ndarray) -> np.ndarray:
        """Transform encoded quantum data back to classical form.
        
        Args:
            encoded_data: Encoded quantum data
            
        Returns:
            Decoded classical data
        """
        pass
    
    def _validate_dimensions(self) -> None:
        """Validate input and output dimensions."""
        if self.input_dim <= 0 or self.output_dim <= 0:
            raise ValueError("Dimensions must be positive integers")