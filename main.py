from core.data_processor import DataProcessor
from core.spectral_analyzer import SpectralAnalyzer
from visualization.plotter import Plotter
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Process astronomical data')
    parser.add_argument('--config', type=str, required=True,
                       help='Path to configuration file')
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    # Initialize components
    data_processor = DataProcessor(config)
    spectral_analyzer = SpectralAnalyzer(config)
    plotter = Plotter(config)
    
    # Process data for each band
    for band in config['data_settings']['datapara']['bands']:
        # Load data cube
        cube = data_processor.load_data_cube(band)
        
        # Load line list
        spectral_analyzer.load_line_list(
            f"{config['data_settings']['paths']['data_dir']}/lines.txt")
        
        # Create plots as specified in config
        if config['graph_settings']['boolean']['spectra_bool']:
            for line in spectral_analyzer.lines:
                plotter.plot_spectrum(
                    cube.frequency_range,
                    cube.data[0, :, 0, 0],  # Example spectrum
                    line.frequency,
                    line.upper_energy
                )
                
        if config['graph_settings']['boolean']['chanmap_bool']:
            # Create moment maps
            pass

if __name__ == '__main__':
    main()