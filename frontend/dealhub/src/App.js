import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';

function App() {
  
  return (<>
    <div className="App">
       <Navbar/>
    </div>
    <div>
    <PriceInfoCard title="Price" iconSrc="/icons/price-icon.png" value="$100" />


    </div>
    </>
  );
}

export default App;
