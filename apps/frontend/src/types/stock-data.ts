// src/types/stockDataTypes.ts
export interface OHLC {
  time: string; // Consider using 'number' for timestamp format
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}

export interface TradeMarker {
  time: string; // Same consideration for time format as OHLC
  position: 'buy' | 'sell';
  label: string;
}

export interface StockData {
  data: OHLC[];
  trades: TradeMarker[];
}
