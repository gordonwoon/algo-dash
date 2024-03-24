// src/components/StockChart.tsx
import React, { useEffect, useRef, useState } from 'react';
import {
  ColorType,
  createChart,
  IChartApi,
  ISeriesApi,
} from 'lightweight-charts';
import { StockData } from '../types';

interface StockChartProps {
  ticker: string;
}

const StockChart: React.FC<StockChartProps> = ({ ticker }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [chart, setChart] = useState<IChartApi | null>(null);

  useEffect(() => {
    if (chartContainerRef.current && !chart) {
      const newChart = createChart(chartContainerRef.current, {
        width: chartContainerRef.current.offsetWidth,
        height: chartContainerRef.current.offsetHeight,
        layout: {
          background: { type: ColorType.Solid, color: '#FFFFFF' },
          textColor: '#333',
        },
        grid: {
          vertLines: {
            color: 'rgba(197, 203, 206, 0.7)',
          },
          horzLines: {
            color: 'rgba(197, 203, 206, 0.7)',
          },
        },
        crosshair: {
          mode: 1, // Corresponds to CrosshairMode.Normal
        },
        // priceScale: {
        //   borderColor: 'rgba(197, 203, 206, 0.8)',
        // },
        timeScale: {
          borderColor: 'rgba(197, 203, 206, 0.8)',
          timeVisible: true,
          secondsVisible: false,
        },
      });
      setChart(newChart);
    }

    return () => {
      chart?.remove();
    };
  }, [chart, ticker]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/stock/${ticker}`);
        if (!response.ok) {
          throw new Error(`API call failed with status: ${response.status}`);
        }
        console.log('res', response);
        const data: StockData = await response.json();
        updateChart(chart, data);
      } catch (error) {
        console.error('Failed to fetch OHLC data:', error);
      }
    };

    if (chart) {
      fetchData();
    }
  }, [chart, ticker]);

  return (
    <div ref={chartContainerRef} style={{ width: '100%', height: '400px' }} />
  );
};

const updateChart = (chart: IChartApi | null, data: StockData): void => {
  if (!chart) return;

  const candleSeries = chart.addCandlestickSeries({
    upColor: '#4bffb5',
    downColor: '#ff4976',
    borderDownColor: '#ff4976',
    borderUpColor: '#4bffb5',
    wickDownColor: '#838ca1',
    wickUpColor: '#838ca1',
  });

  candleSeries.setData(data.ohlc);

  // Add more functionality as needed, such as SMA and trade markers
};

export default StockChart;
