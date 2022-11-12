import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";

export default class LinkSpotify extends Component {
    constructor(props) {
        super(props);

    }

    render() {
        
        return (
            
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography component="body2">
                        AndABirdSang is a simple tool that collects all of the music shared by those you follow on Twitter into a single playlist.
                        The "timeline" is great for some forms of browsing, but often times we miss certain kinds of posts we know we want to see.
                        Shared music is a glaring example. To get started, go on back to the home page. Press start, and we'll have you log in
                        to your Spotify and Twitter accounts. After that, your playlist is just a click away. It's that simple.
                        
                    </Typography>
                    <Typography component="body2">

                        This tool is designed to be a useful repository that users can update every few weeks or so. We suggest
                        that if you like a song in your AndABirdSang playlist, add it to another playlist in your Spotify account, 
                        because that song could disappear soon.

                        Some things to keep in mind:

                        *   we don't keep track of songs you have deleted
                        *   
                    </Typography>

                </Grid>
                <Grid item xs={12} align="center">
                    <Button component={Link} variant="contained" to="/link">
                        BACK
                    </Button>
                </Grid>
                
                
            </Grid>
        
        )
    };
}







