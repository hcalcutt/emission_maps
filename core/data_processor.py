import numpy as np
from astropy.io import fits
from dataclasses import dataclass
from typing import List, Dict, Optional
import json

@dataclass
class DataCube:
    filename: str
    data: np.ndarray
    header: Dict
    frequency_range: np.ndarray
    rms: float

class DataProcessor:
    """Handles loading and processing of astronomical data cubes"""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.data_cubes = {}
        
    def load_data_cube(self, band: str) -> DataCube:
        """Load a data cube for a specific band"""
        cube_path = f"{self.config['data_settings']['paths']['cube_dir']}/{band}/"
        
        # Load fits file
        fits_file = self._get_fits_file(band)
        hdulist = fits.open(f"{cube_path}/{fits_file}")
        
        # Extract key information
        header = hdulist[0].header
        data = fits.getdata(f"{cube_path}/{fits_file}")
        freq_range = self._calculate_frequency_range(header)
        rms = self._calculate_rms(data)
        
        return DataCube(
            filename=fits_file,
            data=data,
            header=header,
            frequency_range=freq_range,
            rms=rms
        )
    
    def _get_fits_file(self, band: str) -> str:
        """Get the appropriate fits file for a band"""
        with open(f"{self.config['data_settings']['paths']['cube_dir']}/{band}/{band}.txt", 'r') as f:
            return f.readline().strip()
            
    def _calculate_frequency_range(self, header: Dict) -> np.ndarray:
        """Calculate the frequency range for a data cube"""
        center_freq = header['CRVAL3'] / 1e9
        spec_res = header['CDELT3'] / 1e9
        n_channels = header['NAXIS3']
        
        return np.linspace(
            center_freq - spec_res * (n_channels/2),
            center_freq + spec_res * (n_channels/2),
            n_channels
        )
    
    def _calculate_rms(self, data: np.ndarray) -> float:
        """Calculate the RMS noise level in the data"""
        # Implement RMS calculation logic
        return np.std(data)

# core/spectral_analyzer.py
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