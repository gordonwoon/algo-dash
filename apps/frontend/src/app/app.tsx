// eslint-disable-next-line @typescript-eslint/no-unused-vars
import styles from './app.module.scss';
import StockChart from './chart';

import NxWelcome from './nx-welcome';

export function App() {
  return (
    <div>
      {/* <NxWelcome title="frontend" /> */}
      <StockChart ticker="AAPL" />
    </div>
  );
}

export default App;
