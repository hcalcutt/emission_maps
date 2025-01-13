from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from scipy.optimize import curve_fit

@dataclass
class SpectralLine:
    frequency: float
    einstein_coeff: float
    quantum_number: str
    upper_energy: float

class SpectralAnalyzer:
    """Handles spectral line analysis"""
    
    def __init__(self, config: dict):
        self.config = config
        self.lines = []
        
    def load_line_list(self, filename: str):
        """Load spectral line information from file"""
        data = np.loadtxt(filename, delimiter='\t')
        
        for line in data:
            if self._meets_threshold(line):
                self.lines.append(SpectralLine(
                    frequency=line[2] / 1000,  # Convert to GHz
                    einstein_coeff=line[4],
                    quantum_number=str(line[0]),
                    upper_energy=line[3]
                ))
                
    def _meets_threshold(self, line: np.ndarray) -> bool:
        """Check if line meets inclusion criteria"""
        return (line[4] > self.config['molecule_settings']['a_thres'] and
                self.config['molecule_settings']['eu_low'] < line[3] < 
                self.config['molecule_settings']['eu_upp'])
    
    def fit_gaussian(self, spectrum: np.ndarray) -> Tuple[float, float, float]:
        """Fit a Gaussian to spectral data"""
        def gaussian(x, amp, cen, wid):
            return amp * np.exp(-(x - cen)**2 / (2 * wid**2))
        
        x = np.arange(len(spectrum))
        popt, _ = curve_fit(gaussian, x, spectrum)
        return popt
