import React from 'react';
//import logo from '../src/img/logo.svg';
import './App.css';
import CustomNavbar from './components/navbar/CustomNavbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home'
import CustomDictionary from './pages/CustomDictionary'
import SearchTwitter from './pages/SearchTwitter'
import SearchTwitterResult from './pages/SearchTwitterResult'
import RecentSearchTwitter from './pages/RecentSearchTwitter'
import PageError from './pages/PageError'
import ProfileGet from './pages/ProfileGet'
import ProfileUpdate from './pages/ProfileUpdate'

function App() {
  return (
    <>
      <Router>
        <CustomNavbar/>
        <Switch>
          <Route path="/" exact component={Home}/>
          <Route path="/customdictionary" component={CustomDictionary}/>
          <Route path="/profile-get" component={ProfileGet}/>
          <Route path="/profile-update" component={ProfileUpdate}/>
          <Route path="/search-twitter" component={SearchTwitter}/>
          <Route path="/search-twitter-result" component={SearchTwitterResult}/>          
          <Route path="/recent-twitter" component={RecentSearchTwitter}/>
          <Route component={PageError}/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
