# visualization/plotter.py
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np
from typing import List, Tuple

class Plotter:
    """Handles all visualization tasks"""
    
    def __init__(self, config: dict):
        self.config = config
        self.setup_matplotlib()
        
    def setup_matplotlib(self):
        """Configure matplotlib settings"""
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.linewidth'] = 1.5
        
    def plot_spectrum(self, 
                     frequencies: np.ndarray, 
                     intensities: np.ndarray,
                     line_freq: float,
                     upper_energy: float) -> None:
        """Plot a spectrum with line markers"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot settings from config
        spec_config = self.config['graph_settings']['specgra_set']
        
        ax.plot(frequencies, intensities, 
                color=spec_config['spectra_linecolour'],
                linewidth=spec_config['linewidth_spec'])
        
        ax.set_xlabel(spec_config['spec_xlabel'])
        ax.set_ylabel(spec_config['spec_ylabel'])
        
        # Add line marker
        ax.axvline(x=line_freq, color='r', linestyle='--')
        
        # Add annotations
        ax.text(0.05, 0.95, f'E_up = {upper_energy:.1f} K',
                transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(f"{self.config['data_settings']['paths']['plot_dir']}/spectrum.png")
        plt.close()
        
    def plot_moment_map(self, 
                       data: np.ndarray,
                       contour_levels: List[float],
                       beam_size: float) -> None:
        """Plot a moment map with contours"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        map_config = self.config['graph_settings']['chanmap_set']
        
        # Plot contours
        ax.contour(data, levels=contour_levels,
                  cmap='viridis')
        
        # Add beam size indicator
        self._add_beam(ax, beam_size)
        
        # Set limits
        ax.set_xlim(map_config['map_xliml'], map_config['map_xlimu'])
        ax.set_ylim(map_config['map_yliml'], map_config['map_ylimu'])
        
        plt.savefig(f"{self.config['data_settings']['paths']['plot_dir']}/moment_map.png")
        plt.close()
        
    def _add_beam(self, ax: plt.Axes, beam_size: float):
        """Add beam size indicator to plot"""
        beam = Circle((0.9, 0.9), beam_size/2, 
                     transform=ax.transAxes, 
                     facecolor='gray',
                     alpha=0.5)
        ax.add_artist(beam)