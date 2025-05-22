import React, { useState, useEffect } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
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
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ElementModule = () => {
  const [selectedElement, setSelectedElement] = useState('U');
  const [selectedProperty, setSelectedProperty] = useState('half_life');
  const [chartData, setChartData] = useState(null);

  // Element data (similar to Python version)
  const elements = {
    'U': { name: 'Uran', half_life: 4.5e9, state: 'Stały', activation_energy: 0.52, melting_point: 1405, boiling_point: 4404 },
    'Pu': { name: 'Pluton', half_life: 2.4e4, state: 'Stały', activation_energy: 0.57, melting_point: 912, boiling_point: 3505 },
    'Th': { name: 'Tor', half_life: 1.4e10, state: 'Stały', activation_energy: 0.58, melting_point: 2023, boiling_point: 5061 },
    'Ra': { name: 'Rad', half_life: 1.6e3, state: 'Stały', activation_energy: 0.48, melting_point: 973, boiling_point: 2010 },
    'Rn': { name: 'Radon', half_life: 3.8, state: 'Gazowy', activation_energy: 0.36, melting_point: 202, boiling_point: 211 },
    'Po': { name: 'Polon', half_life: 138, state: 'Stały', activation_energy: 0.41, melting_point: 527, boiling_point: 1235 },
    'Bi': { name: 'Bizmut', half_life: 2.0e19, state: 'Stały', activation_energy: 0.43, melting_point: 544, boiling_point: 1837 },
    'Pb': { name: 'Ołów', half_life: Infinity, state: 'Stały', activation_energy: 0.37, melting_point: 600, boiling_point: 2022 },
    'Tl': { name: 'Tal', half_life: Infinity, state: 'Stały', activation_energy: 0.33, melting_point: 577, boiling_point: 1746 },
    'Hg': { name: 'Rtęć', half_life: Infinity, state: 'Ciekły', activation_energy: 0.29, melting_point: 234, boiling_point: 630 }
  };

  useEffect(() => {
    updateChart();
  }, [selectedElement, selectedProperty]);

  const updateChart = () => {
    if (selectedProperty === 'half_life') {
      // Create bar chart for half-lives
      const elementData = Object.entries(elements)
        .filter(([_, data]) => data.half_life !== Infinity)
        .sort((a, b) => b[1].half_life - a[1].half_life);

      setChartData({
        labels: elementData.map(([symbol]) => symbol),
        datasets: [{
          label: 'Half-life (years)',
          data: elementData.map(([_, data]) => data.half_life),
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          borderColor: 'rgb(53, 162, 235)',
          borderWidth: 1
        }]
      });
    } else {
      // Create line chart for temperature-dependent properties
      const temperatures = Array.from({ length: 50 }, (_, i) => 300 + i * 100);
      const propertyValues = temperatures.map(temp => {
        const baseValue = elements[selectedElement][selectedProperty];
        // Simulate temperature dependence
        return baseValue * (1 + 0.0001 * (temp - 300));
      });

      setChartData({
        labels: temperatures,
        datasets: [{
          label: getPropertyLabel(selectedProperty),
          data: propertyValues,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          tension: 0.1
        }]
      });
    }
  };

  const getPropertyLabel = (property) => {
    switch (property) {
      case 'half_life': return 'Half-life (years)';
      case 'activation_energy': return 'Activation Energy (eV)';
      case 'melting_point': return 'Melting Point (K)';
      case 'boiling_point': return 'Boiling Point (K)';
      default: return property;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex space-x-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700">Element</label>
          <select
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={selectedElement}
            onChange={(e) => setSelectedElement(e.target.value)}
          >
            {Object.entries(elements).map(([symbol, data]) => (
              <option key={symbol} value={symbol}>
                {symbol} - {data.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700">Property</label>
          <select
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={selectedProperty}
            onChange={(e) => setSelectedProperty(e.target.value)}
          >
            <option value="half_life">Half-life</option>
            <option value="activation_energy">Activation Energy</option>
            <option value="melting_point">Melting Point</option>
            <option value="boiling_point">Boiling Point</option>
          </select>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        {chartData && (
          selectedProperty === 'half_life' ? (
            <Bar
              data={chartData}
              options={{
                responsive: true,
                plugins: {
                  legend: { position: 'top' },
                  title: {
                    display: true,
                    text: 'Element Half-lives'
                  }
                },
                scales: {
                  y: {
                    type: 'logarithmic',
                    title: {
                      display: true,
                      text: 'Years'
                    }
                  }
                }
              }}
            />
          ) : (
            <Line
              data={chartData}
              options={{
                responsive: true,
                plugins: {
                  legend: { position: 'top' },
                  title: {
                    display: true,
                    text: `${getPropertyLabel(selectedProperty)} vs Temperature`
                  }
                },
                scales: {
                  x: {
                    title: {
                      display: true,
                      text: 'Temperature (K)'
                    }
                  },
                  y: {
                    title: {
                      display: true,
                      text: getPropertyLabel(selectedProperty)
                    }
                  }
                }
              }}
            />
          )
        )}
      </div>

      <div className="mt-4 bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Element Properties</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">State</p>
            <p className="text-sm font-medium text-gray-900">{elements[selectedElement].state}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Activation Energy</p>
            <p className="text-sm font-medium text-gray-900">{elements[selectedElement].activation_energy} eV</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Melting Point</p>
            <p className="text-sm font-medium text-gray-900">{elements[selectedElement].melting_point} K</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Boiling Point</p>
            <p className="text-sm font-medium text-gray-900">{elements[selectedElement].boiling_point} K</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ElementModule;