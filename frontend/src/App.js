import React from 'react';
//import logo from '../src/img/logo.svg';
import './App.css';
import NavBar from './components/sections/navbar/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home'
import Search from './pages/Search'
import CustomDictionary from './pages/CustomDictionary'
import RecentSearch from './pages/RecentSearch'
import PageError from './pages/PageError'

function App() {
  return (
    <>
      <Router>
        <NavBar/>
        <Switch>
          <Route path="/" exact component={Home}/>
          <Route path="/search" component={Search}/> 
          <Route path="/customdictionary" component={CustomDictionary}/> 
          <Route path="/recentsearch" component={RecentSearch}/>
          <Route component={PageError}/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
