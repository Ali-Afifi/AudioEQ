# AudioEQ: Interactive Audio Equalizer

**AudioEQ** is an interactive audio equalizer built using Python. It allows users to upload `.wav` or `.csv` files, visualize audio data, apply frequency-specific adjustments using sliders, and export the processed audio. The application is powered by the Panel library and features a user-friendly web-based interface.

## Features
- Upload and process `.wav` and `.csv` audio files.
- Visualize input and output audio waveforms with interactive graphs.
- Customize frequency gains using sliders for specific frequency bands (e.g., 20Hz–40Hz, 40Hz–80Hz).
- Generate spectrograms for detailed frequency analysis.
- Export processed audio files.

## Technologies Used
- **Panel**: For building interactive web applications.
- **Bokeh**: For plotting graphs and visualizations.
- **Librosa**: For audio processing and feature extraction.
- **Matplotlib**: For generating spectrograms.
- **SciPy**: For Fourier transforms and other signal processing tasks.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Ali-Afifi/AudioEQ.git
   cd AudioEQ
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python -m panel serve --dev --autoreload --port 8080 app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8080/app
   ```

3. Upload an audio file (`.wav` or `.csv`), adjust the sliders to modify the audio, and export the processed file.

## How It Works
1. **Audio Upload**:
   - Supports `.wav` and `.csv` file formats.
   - Extracts and visualizes audio amplitude over time.

2. **Interactive Equalizer**:
   - Sliders allow you to apply gain to specific frequency bands.
   - Modes include:
     - **Default**: Basic equalization.
     - **Music**: Optimized for music tracks.
     - **Vocals**: Optimized for vocal tracks.

3. **Spectrograms**:
   - View spectrograms of input and processed audio for detailed frequency visualization.

4. **Output**:
   - Processed audio can be saved in `.wav` format.

## Dependencies
The project requires the following Python libraries:
- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `bokeh==2.4.3`
- `soundfile`
- `panel==0.14.1`
- `hvplot`
- `librosa`
- `ipympl`

These can be installed using the `requirements.txt` file.

## Project Structure
- `app.py`: Main application script.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## Screenshots
_Add screenshots of the application's interface and visualizations here._

## Contribution
Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements.

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.
