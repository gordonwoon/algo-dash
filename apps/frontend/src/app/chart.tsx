import React, { useEffect, useRef } from 'react';
import { createChart, IChartApi, ISeriesApi } from 'lightweight-charts';
import { StockData } from '../types';

interface StockChartProps {
  ticker: string;
}

const StockChart: React.FC<StockChartProps> = ({ ticker }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  useEffect(() => {
    if (chartContainerRef.current && !chartRef.current) {
      const newChart = createChart(chartContainerRef.current, {
        width: chartContainerRef.current.offsetWidth,
        height: chartContainerRef.current.offsetHeight,
      });
      chartRef.current = newChart;
    }

    return () => {
      // Cleanup the chart and ensure no attempt to use the chart after this point
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    const fetchDataAndUpdateChart = async () => {
      try {
        const response = await fetch(`/api/stock/${ticker}`);
        if (!response.ok) {
          throw new Error(`API call failed with status: ${response.status}`);
        }
        const data: StockData = await response.json();

        if (chartRef.current) {
          // If there's an existing series, remove it before creating a new one
          if (seriesRef.current) {
            chartRef.current.removeSeries(seriesRef.current);
            seriesRef.current = null;
          }

          // Add new series to the chart
          const candleSeries = chartRef.current.addCandlestickSeries();
          candleSeries.setData(data.data);
          seriesRef.current = candleSeries;
        }
      } catch (error) {
        console.error('Failed to fetch OHLC data:', error);
      }
    };

    if (chartRef.current) {
      fetchDataAndUpdateChart();
    }
  }, [ticker]);

  return (
    <div ref={chartContainerRef} style={{ width: '100%', height: '400px' }} />
  );
};

export default StockChart;
