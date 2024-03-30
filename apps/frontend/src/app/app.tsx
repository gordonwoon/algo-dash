// eslint-disable-next-line @typescript-eslint/no-unused-vars
import styles from './app.module.scss';
import StockChart from './chart';

export function App() {
  return (
    <div>
      <StockChart ticker="AAPL" />
    </div>
  );
}

export default App;
