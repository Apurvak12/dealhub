import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Home from './components/Home';

function App() {
  
  return (
    <div className="App">
       <Navbar/>
       <Home/>
       <Hero/>
    </div>
  );
}

export default App;
