import React from 'react';
//import logo from '../src/img/logo.svg';
import './App.css';
import CustomNavbar from './components/navbar/CustomNavbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home'
import Search from './pages/Search'
import CustomDictionary from './pages/CustomDictionary'
import SearchTwitter from './pages/SearchTwitter'
import RecentSearchTwitter from './pages/RecentSearchTwitter'
import PageError from './pages/PageError'
import Profile from './pages/Profile'

function App() {
  return (
    <>
      <Router>
        <CustomNavbar/>
        <Switch>
          <Route path="/" exact component={Home}/>
          <Route path="/search" component={Search}/> 
          <Route path="/customdictionary" component={CustomDictionary}/> 
          <Route path="/profile" component={Profile}/>
          <Route path="/search-twitter" component={SearchTwitter}/>
          <Route path="/recent-twitter" component={RecentSearchTwitter}/>          
          <Route component={PageError}/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
