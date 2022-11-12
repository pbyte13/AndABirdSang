import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Link from "./Link";
import HowItWorks from "./HowItWorks";
import CreatePlaylist from "./CreatePlaylist";
import ProgressBar from "./ProgressBar";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
        

        };


    render() {
        return (
          <Router>
            <Switch>
              
              <Route path="/link" component={Link} />
              <Route path="/create" component={CreatePlaylist} />
              <Route path="/how-it-works" component={HowItWorks} />
              <Route path='/progress/:taskID' component={ProgressBar} />
             
            </Switch>
          </Router>
        );
      }
}