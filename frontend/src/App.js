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
          <Route exact path="/customdictionary" component={CustomDictionary}/>
          <Route exact path="/profile-get" component={ProfileGet}/>
          <Route exact path="/profile-update" component={ProfileUpdate}/>
          <Route exact path="/search-twitter" component={SearchTwitter}/>
          <Route exact path="/search-twitter-result" component={SearchTwitterResult}/>          
          <Route exact path="/recent-twitter" component={RecentSearchTwitter}/>
          <Route component={PageError}/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
