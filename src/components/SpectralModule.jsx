import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SpectralModule = () => {
  const [spectrumType, setSpectrumType] = useState('emission');
  const [filterAlgorithm, setFilterAlgorithm] = useState('kalman');
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    generateSampleData();
  }, [spectrumType, filterAlgorithm]);

  const generateSampleData = () => {
    // Generate wavelengths from 300 to 1000 nm
    const wavelengths = Array.from({ length: 100 }, (_, i) => 300 + i * 7);
    
    // Generate spectrum data based on type
    let intensities;
    if (spectrumType === 'emission') {
      intensities = wavelengths.map(w => {
        let value = 0;
        [350, 450, 550, 650, 750].forEach(peak => {
          value += 100 * Math.exp(-(w - peak)**2 / (2 * 100));
        });
        return value + Math.random() * 5;
      });
    } else if (spectrumType === 'absorption') {
      intensities = wavelengths.map(w => 100 - (100 * Math.exp(-(w - 550)**2 / (2 * 100))) + Math.random() * 5);
    } else {
      intensities = wavelengths.map(w => 50 + 30 * Math.sin(0.1 * w) + Math.random() * 3);
    }

    // Apply filter if selected
    const filteredIntensities = applyFilter(intensities, filterAlgorithm);

    setChartData({
      labels: wavelengths,
      datasets: [
        {
          label: `${spectrumType.charAt(0).toUpperCase() + spectrumType.slice(1)} Spectrum`,
          data: filteredIntensities,
          borderColor: spectrumType === 'emission' ? 'rgb(255, 99, 132)' : 
                      spectrumType === 'absorption' ? 'rgb(53, 162, 235)' : 
                      'rgb(75, 192, 192)',
          backgroundColor: 'rgba(255, 255, 255, 0.5)',
        }
      ]
    });
  };

  const applyFilter = (data, filterType) => {
    switch (filterType) {
      case 'kalman':
        return kalmanFilter(data);
      case 'gaussian':
        return gaussianFilter(data);
      case 'median':
        return medianFilter(data);
      default:
        return data;
    }
  };

  const kalmanFilter = (data) => {
    const filtered = [data[0]];
    const kalmanGain = 0.75;
    for (let i = 1; i < data.length; i++) {
      filtered.push(filtered[i-1] + kalmanGain * (data[i] - filtered[i-1]));
    }
    return filtered;
  };

  const gaussianFilter = (data) => {
    const windowSize = 5;
    const sigma = 1;
    return data.map((_, i) => {
      let sum = 0;
      let weightSum = 0;
      for (let j = Math.max(0, i - windowSize); j < Math.min(data.length, i + windowSize + 1); j++) {
        const weight = Math.exp(-(i - j)**2 / (2 * sigma**2));
        sum += data[j] * weight;
        weightSum += weight;
      }
      return sum / weightSum;
    });
  };

  const medianFilter = (data) => {
    const windowSize = 5;
    return data.map((_, i) => {
      const window = data.slice(
        Math.max(0, i - Math.floor(windowSize/2)),
        Math.min(data.length, i + Math.floor(windowSize/2) + 1)
      ).sort((a, b) => a - b);
      return window[Math.floor(window.length/2)];
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex space-x-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700">Spectrum Type</label>
          <select
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={spectrumType}
            onChange={(e) => setSpectrumType(e.target.value)}
          >
            <option value="emission">Emission</option>
            <option value="absorption">Absorption</option>
            <option value="interferometric">Interferometric</option>
          </select>
        </div>
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700">Filter Algorithm</label>
          <select
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={filterAlgorithm}
            onChange={(e) => setFilterAlgorithm(e.target.value)}
          >
            <option value="kalman">Kalman Filter</option>
            <option value="gaussian">Gaussian Filter</option>
            <option value="median">Median Filter</option>
            <option value="none">No Filter</option>
          </select>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        {chartData && (
          <Line
            data={chartData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: 'Spectral Analysis'
                }
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: 'Wavelength (nm)'
                  }
                },
                y: {
                  title: {
                    display: true,
                    text: 'Intensity'
                  }
                }
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default SpectralModule;