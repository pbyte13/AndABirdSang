import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText, { Card } from "@material-ui/core";
import FormControl from "@material-ui/core/FormControl";

export default class LinkSpotify extends Component {
    constructor(props) {
        super(props);
        this.state = {
            //spotifyAuthenticated: false,

        };

        this.handleStartButtonPressed = this.handleStartButtonPressed.bind(this);
        //this.authenticateSpotify = this.authenticateSpotify.bind(this);
        //this.authenticateSpotify();

    }

    handleStartButtonPressed() {
        fetch("/spotify/get-auth-url")
        // the view associated with /spotify/get-auth-url redirects to twitter auth flow
        .then((response) => response.json())
        .then((data) => {
            window.location.replace(data.url);
        })
        
    }

    render() {
        
        return (
            
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                        AndABirdSang
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="body1">
                        generate a personal playlist of songs shared by people you follow on Twitter
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center" onClick={this.handleStartButtonPressed}>
                    <Button variant="contained" color="success">
                        START
                    </Button>
                </Grid>

                <Grid item xs={12} align="center">
                    <Button component={Link} to="/how-it-works">
                        HOW IT WORKS
                    </Button>
                </Grid>
                
                
            </Grid>
        
        )
    };
}